function wbauto()
% wbauto - static-configuration grid for the SSV revision (round 3).
%
%   Environment:
%     WBTASK3  : index of the configuration to run (1..NC)      [required]
%     WNSEED   : global seed cap (default 30); per-problem caps apply as well
%     WBFE     : evaluation budget (default 100000)
%
%   Each invocation handles ONE configuration over all problems and seeds,
%   so configurations run as independent processes.  Resumable.
%   Archive: results/wbauto/wbA_<CI>.mat
%   Log    : results/wbauto/wbA_<CI>_progress.txt

t_start = tic;
CI = str2double(getenv('WBTASK3'));
if isnan(CI) || CI < 1, error('WBTASK3 must be a positive integer'); end
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
if CI > numel(CFG), error('WBTASK3=%d exceeds %d configs', CI, numel(CFG)); end
c  = CFG{CI};
nP = numel(PR);
WNP = getenv('WNPMAX'); if ~isempty(WNP), nP = min(nP, str2double(WNP)); end

OD = 'results/wbauto';
if ~exist(OD,'dir'), mkdir(OD); end
MF = fullfile(OD, sprintf('wbA_%02d.mat', CI));
TF = fullfile(OD, sprintf('wbA_%02d_progress.txt', CI));

A = struct('name', c.name, 'igd', {cell(nP,1)}, 'objs', {cell(nP,1)}, ...
           'fe', {cell(nP,1)}, 'gen', {cell(nP,1)}, 'tim', {cell(nP,1)});
if exist(MF,'file')
    S = load(MF,'A');
    if isfield(S,'A') && numel(S.A.igd) == nP, A = S.A; end
end
logline(TF, sprintf('=== wbauto cfg=%d (%s) FE=%d nseed<=%d | %s ===', CI, c.name, WNFE, WNS, datestr(now)));

for pp = 1:nP
    sname = PR{pp}{1}; sM = PR{pp}{2}; sD = PR{pp}{3}; sNS = min(PR{pp}{4}, WNS);
    if numel(A.igd{pp}) ~= sNS
        A.igd{pp} = nan(1,sNS); A.objs{pp} = cell(1,sNS); A.fe{pp} = nan(1,sNS);
        A.gen{pp} = nan(1,sNS); A.tim{pp} = nan(1,sNS);
    end
    for ss = 1:sNS
        if ~isnan(A.igd{pp}(ss)), continue; end
        try
            rng(ss);
            F = feval(sname, 'M', sM, 'D', sD);
            F.Setting(); F.maxFE = WNFE;
            t0 = tic;
            Mth = make_method(c, F, sM);
            Mth.Solve(F);
            Pn  = Mth.result{end};
            PF  = feval(sname, 'M', sM, 'D', sD).GetOptimum(400);
            A.igd{pp}(ss) = myIGD(Pn.objs, PF, Pn.cons);
            A.objs{pp}{ss} = Pn.objs;
            A.fe{pp}(ss)  = F.FE;
            A.tim{pp}(ss) = toc(t0);
            if isfield(Mth,'hist') && isstruct(Mth.hist) && isfield(Mth.hist,'generations')
                A.gen{pp}(ss) = Mth.hist.generations;
            end
            save(MF,'A');
            logline(TF, sprintf('[%s %s M%dD%d s%02d] igd=%.5f fe=%d tim=%.1fs', ...
                    c.name, sname, sM, sD, ss, A.igd{pp}(ss), F.FE, A.tim{pp}(ss)));
        catch e
            logline(TF, sprintf('[%s %s M%dD%d s%02d] FAIL: %s', ...
                    c.name, sname, sM, sD, ss, e.message));
        end
    end
end
logline(TF, sprintf('=== DONE cfg=%d in %.1fs ===', CI, toc(t_start)));
disp('WBAUTO_DONE');
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
    case 'FDSEA_ssv_ctrl'
        Mth = FDSEA_ssv_ctrl('save',0,'outputFcn',@(a,q) []);
        Mth.ssvSig = c.sig; Mth.ssvCtrl = c.ctrl; Mth.ssvAlpha = 0.05; Mth.ssvKAlpha = 1;
        Mth.ssvKMin = 5; Mth.ssvExchDamp = 1; Mth.ssvGamaDir = c.gdir; Mth.ssvRec = 1;
    otherwise
        error('unknown class %s', c.cls);
end
end

function C = cfglist()
% name, class, exchange, gamma(0=host rule), order, N-mode, ref-mode,
% signal, control, regime direction
mk = @(n,cl,x,g,k,m,r,s,c,gd) struct('name',n,'cls',cl,'nexch',x,'gama',g,'K',k, ...
        'Nmode',m,'refmode',r,'sig',s,'ctrl',c,'gdir',gd);
C = { ...
 mk('hostNBI','FDSEA',         NaN, NaN, 5, NaN, NaN, NaN, NaN, NaN), ...  % published host
 mk('hostN',  'FDSEA_cfg',      10,   0, 5,   0,   0, NaN, NaN, NaN), ...  % fix 1: keep requested N
 mk('hostMUD','FDSEA_cfg',      10,   0, 5,   0,   1, NaN, NaN, NaN), ...  % fix 2: exactly-N vectors
 mk('layer',  'FDSEA_ssv_ctrl', NaN, NaN, 5, NaN, NaN,   1,   0,   0), ...  % adaptive layer (auto delta)
 mk('e5g0',   'FDSEA_cfg',       5,   0, 5,   0,   0, NaN, NaN, NaN), ...
 mk('e5g7',   'FDSEA_cfg',       5, 0.7, 5,   0,   0, NaN, NaN, NaN), ...
 mk('e5g3',   'FDSEA_cfg',       5, 0.3, 5,   0,   0, NaN, NaN, NaN), ...
 mk('e10g7',  'FDSEA_cfg',      10, 0.7, 5,   0,   0, NaN, NaN, NaN), ...
 mk('e20g0',  'FDSEA_cfg',      20,   0, 5,   0,   0, NaN, NaN, NaN), ...
 };
end

function PR = problist()
% {problem, M, D, nseeds}
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
