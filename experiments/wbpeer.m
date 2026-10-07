function wbpeer()
% wbpeer - cross-algorithm consequence of the population-size override.
% Compares three reference-vector peers with the published override and with
% the requested population size kept.  Env: WBTASK4 = config index (1..6).
cd('D:\harness工作\中国科学：数学(总)\算法\algorithm');
P = '_tmp_official/PlatEMO-master/PlatEMO';
p = strsplit(path,';'); keep = ~contains(p,'Huawei_Cup','IgnoreCase',true); path(strjoin(p(keep),';'));
addpath(genpath([P '/Algorithms'])); addpath(genpath([P '/Problems'])); addpath(genpath([P '/Metrics']));
addpath('algorithms'); addpath('algorithms/FDSEA'); addpath('algorithms/nofix'); addpath('D:\wb_run');
warning('off','all'); set(0,'DefaultFigureVisible','off');

CI = str2double(getenv('WBTASK4'));
WNFE = 100000; WNS = 30;
% config -> (algorithm, problem set)
CONF = { {'NSGAIII',  1}, {'NSGAIII_N', 1}, ...
         {'MOEAD',    2}, {'MOEAD_N',   2} };
% problem set 1 = six LSMOP instances (NSGA-III), set 2 = LSMOP1 only (MOEA/D is slow)
PRSET = { { {'LSMOP1',3,300}, {'LSMOP2',3,300}, {'LSMOP4',3,300}, ...
            {'LSMOP6',3,300}, {'LSMOP8',3,300}, {'LSMOP9',3,300} }, ...
          { {'LSMOP1',3,300} } };
CLS = CONF{CI}{1}; PR = PRSET{CONF{CI}{2}};
nP = numel(PR); OD = 'results/wbpeer'; if ~exist(OD,'dir'), mkdir(OD); end
MF = fullfile(OD, sprintf('wbP_%02d.mat', CI));
TF = fullfile(OD, sprintf('wbP_%02d_progress.txt', CI));

A = struct('name', CLS, 'igd', {cell(nP,1)}, 'fe', {cell(nP,1)}, ...
           'gen', {cell(nP,1)}, 'tim', {cell(nP,1)});
if exist(MF,'file'), S = load(MF,'A'); if isfield(S,'A'), A = S.A; end; end
logline(TF, sprintf('=== wbpeer cfg=%d (%s) | %s ===', CI, CLS, datestr(now)));

for pp = 1:nP
    if numel(A.igd{pp}) ~= WNS
        A.igd{pp} = nan(1,WNS); A.fe{pp} = nan(1,WNS); A.gen{pp} = nan(1,WNS); A.tim{pp} = nan(1,WNS);
    end
    for ss = 1:WNS
        if ~isnan(A.igd{pp}(ss)), continue; end
        try
            rng(ss);
            F = feval(PR{pp}{1},'M',PR{pp}{2},'D',PR{pp}{3}); F.Setting(); F.maxFE = WNFE;
            t0 = tic;
            Mth = feval(CLS, 'save',0,'outputFcn',@(a,q) []);
            Mth.Solve(F);
            Pn = Mth.result{end};
            PF = feval(PR{pp}{1},'M',PR{pp}{2},'D',PR{pp}{3}).GetOptimum(400);
            A.igd{pp}(ss) = myIGD(Pn.objs, PF, Pn.cons);
            A.fe{pp}(ss) = F.FE; A.tim{pp}(ss) = toc(t0);
            save(MF,'A');
            logline(TF, sprintf('[%s %s s%02d] igd=%.5f fe=%d tim=%.1fs', CLS, PR{pp}{1}, ss, A.igd{pp}(ss), F.FE, A.tim{pp}(ss)));
        catch e
            logline(TF, sprintf('[%s %s s%02d] FAIL: %s', CLS, PR{pp}{1}, ss, e.message));
        end
    end
end
logline(TF, sprintf('=== DONE cfg=%d ===', CI));
disp('WBPEER_DONE');
end
function logline(f,s), fid=fopen(f,'a'); fprintf(fid,'%s\n',s); fclose(fid); end
