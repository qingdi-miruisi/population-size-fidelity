function wb13()
% wb13 -- round-13 experiments for the SCIS submission.
%
%   Adds the three arms the domain review asked for and a K sweep:
%     hostA  : the published host configured at the size it will actually
%              realise (91 at M=3, 85 at M=5), i.e. declared == realised.
%              Together with hostNBI (declared 100, realised 91) and
%              hostN (declared 100, realised 100) this gives the A/B/C design.
%     k3, k10: the static setting (n_ex=10, gamma=0.7) with K=3 and K=10,
%              completing the K in {3,5,10} sweep against the existing e10g7 (K=5).
%
%   Environment: WB13CI  index of the configuration (required)
%                WBFE   evaluation budget (default 100000)
%                WNSEED global seed cap (default 30)
%
%   Archive: results/wbround13/wbB_<CI>.mat   (never touches earlier results)

t_start = tic;
CI = str2double(getenv('WB13CI'));
if isnan(CI) || CI < 1, error('WB13CI must be a positive integer'); end
WNFE = getenv('WBFE');   if isempty(WNFE), WNFE = 100000; else, WNFE = str2double(WNFE); end
WNS  = getenv('WNSEED'); if isempty(WNS),  WNS  = 30;     else, WNS  = str2double(WNS); end

cd('D:\harness工作\中国科学：数学(总)\算法\algorithm');
P = '_tmp_official/PlatEMO-master/PlatEMO';
p = strsplit(path,';'); keep = ~contains(p,'Huawei_Cup','IgnoreCase',true); path(strjoin(p(keep),';'));
addpath(genpath([P '/Algorithms'])); addpath(genpath([P '/Problems'])); addpath(genpath([P '/Metrics']));
addpath('algorithms'); addpath('algorithms/FDSEA'); addpath('D:\wb_run');
warning('off','all'); set(0,'DefaultFigureVisible','off');

CFG = cfglist();
PR  = problist();
if CI > numel(CFG), error('WB13CI=%d exceeds %d configs', CI, numel(CFG)); end
c  = CFG{CI};
nP = numel(PR);

OD = 'results/wbround13';
if ~exist(OD,'dir'), mkdir(OD); end
MF = fullfile(OD, sprintf('wbB_%02d.mat', CI));
TF = fullfile(OD, sprintf('wbB_%02d_progress.txt', CI));

A = struct('name', c.name, 'igd', {cell(nP,1)}, 'objs', {cell(nP,1)}, ...
           'fe', {cell(nP,1)}, 'gen', {cell(nP,1)}, 'tim', {cell(nP,1)}, ...
           'Nreq', {cell(nP,1)}, 'Nreal', {cell(nP,1)});
if exist(MF,'file')
    S = load(MF,'A');
    if isfield(S,'A') && numel(S.A.igd) == nP, A = S.A; end
end
logline(TF, sprintf('=== wb13 cfg=%d (%s) FE=%d nseed<=%d | %s ===', CI, c.name, WNFE, WNS, datestr(now)));

for pp = 1:nP
    sname = PR{pp}{1}; sM = PR{pp}{2}; sD = PR{pp}{3}; sNS = min(PR{pp}{4}, WNS);
    if numel(A.igd{pp}) ~= sNS
        A.igd{pp} = nan(1,sNS); A.objs{pp} = cell(1,sNS); A.fe{pp} = nan(1,sNS);
        A.gen{pp} = nan(1,sNS); A.tim{pp} = nan(1,sNS);
        A.Nreq{pp} = nan(1,sNS); A.Nreal{pp} = nan(1,sNS);
    end
    for ss = 1:sNS
        if ~isnan(A.igd{pp}(ss)), continue; end
        try
            rng(ss);
            F = feval(sname, 'M', sM, 'D', sD);
            F.Setting();
            % configured population size for this arm
            if strcmp(c.Npolicy,'realised')
                [~,F.N] = UniformPoint(100, sM);   % declare what will be realised
            else
                F.N = 100;
            end
            F.maxFE = WNFE;
            nreq    = F.N;
            t0 = tic;
            Mth = make_method(c, F, sM);
            Mth.Solve(F);
            Pn  = Mth.result{end};
            PF  = feval(sname, 'M', sM, 'D', sD).GetOptimum(400);
            A.igd{pp}(ss)  = myIGD(Pn.objs, PF, Pn.cons);
            A.objs{pp}{ss} = Pn.objs;
            A.fe{pp}(ss)   = F.FE;
            A.tim{pp}(ss)  = toc(t0);
            A.Nreq{pp}(ss) = nreq;
            A.Nreal{pp}(ss)= size(Pn.objs,1);   % realised population of the final state
            if isfield(Mth,'hist') && isstruct(Mth.hist) && isfield(Mth.hist,'generations')
                A.gen{pp}(ss) = Mth.hist.generations;
            end
            save(MF,'A');
            logline(TF, sprintf('[%s %s M%dD%d s%02d] Nreq=%d Nreal=%d igd=%.5f fe=%d tim=%.1fs', ...
                    c.name, sname, sM, sD, ss, nreq, A.Nreal{pp}(ss), A.igd{pp}(ss), F.FE, A.tim{pp}(ss)));
        catch e
            logline(TF, sprintf('[%s %s M%dD%d s%02d] FAIL: %s', ...
                    c.name, sname, sM, sD, ss, e.message));
        end
    end
end
logline(TF, sprintf('=== DONE cfg=%d in %.1fs ===', CI, toc(t_start)));
disp('WB13_DONE');
end

% ---------------------------------------------------------------- helpers
function Mth = make_method(c, F, M) %#ok<INUSD>
switch c.cls
    case 'FDSEA'
        Mth = FDSEA('save',0,'outputFcn',@(a,q) []);
    case 'FDSEA_cfg'
        Mth = FDSEA_cfg('save',0,'outputFcn',@(a,q) []);
        Mth.nexch = c.nexch; Mth.gama = c.gama; Mth.K0 = c.K; Mth.Nmode = c.Nmode;
        Mth.refmode = c.refmode; Mth.rec = 1;
    otherwise
        error('unknown class %s', c.cls);
end
end

function C = cfglist()
% name, class, exchange, gamma, K, N-mode, ref-mode, N-policy
mk = @(n,cl,x,g,k,m,r,np) struct('name',n,'cls',cl,'nexch',x,'gama',g,'K',k, ...
        'Nmode',m,'refmode',r,'Npolicy',np);
C = { ...
 mk('hostA','FDSEA',        NaN, NaN, 5, NaN, NaN, 'realised'), ...  % declared == realised
 mk('k3',   'FDSEA_cfg',     10, 0.7, 3,   0,   0, 'req'), ...      % K sweep
 mk('k10',  'FDSEA_cfg',     10, 0.7, 10,  0,   0, 'req'), ...      % K sweep
 };
end

function PR = problist()
% {problem, M, D, nseeds}   -- identical to the round-3 suite, same seeds
PR = { ...
 {'DTLZ1',3,300,30}, {'DTLZ2',3,300,30}, {'DTLZ7',3,300,30}, ...
 {'LSMOP1',3,300,30}, {'LSMOP2',3,300,30}, {'LSMOP3',3,300,30}, ...
 {'LSMOP4',3,300,30}, {'LSMOP5',3,300,30}, {'LSMOP6',3,300,30}, ...
 {'LSMOP7',3,300,30}, {'LSMOP8',3,300,30}, {'LSMOP9',3,300,30}, ...
 {'LSMOP1',5,500,20}, {'LSMOP6',5,500,20}, {'LSMOP1',3,1000,20} };
end

function logline(f, s)
fid = fopen(f,'a'); fprintf(fid,'%s\n', s); fclose(fid);
end
