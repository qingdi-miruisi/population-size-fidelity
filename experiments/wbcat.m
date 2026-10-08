function wbcat()
% wbcat - catalogue validation for repair cases B and C (Table S7).
% Arms: *_PUB = published override (the constructor write-back takes effect);
%       *_MUD = repair 2, the exactly-N MUD constructor;
%       *_BA  = the bounded-angle exactly-N constructor (Case C repair);
%       RVEA_N (algorithms/nofix) = RVEA under repair 2.
% Problems: DTLZ1-7 at M = 3 with the release default D = M+4, requested
% N = 100, budget 1e5 evaluations, seeds 1..30, single-threaded.
% Env: WBCAT_CFG = config index (1..8). Each run is saved as it completes,
% so the driver resumes after an interruption.
cd('D:\harness工作\中国科学：数学(总)\算法\algorithm');
P = '_tmp_official/PlatEMO-master/PlatEMO';
p = strsplit(path,';'); keep = ~contains(p,'Huawei_Cup','IgnoreCase',true); path(strjoin(p(keep),';'));
addpath(genpath(P)); addpath('algorithms'); addpath(genpath('algorithms/cat')); addpath('algorithms/nofix');
warning('off','all'); set(0,'DefaultFigureVisible','off');

CI = str2double(getenv('WBCAT_CFG'));
WNFE = 100000; WNS = 30;
CONF = {'MOEAD_PUB','MOEAD_MUD','RVEA_PUB','RVEA_N','RVEA_BA','LMOCSO_PUB','LMOCSO_MUD','LMOCSO_BA'};
CLS = CONF{CI};
PR = {'DTLZ1','DTLZ2','DTLZ3','DTLZ4','DTLZ5','DTLZ6','DTLZ7'};
nP = numel(PR); OD = 'results/wbcat'; if ~exist(OD,'dir'), mkdir(OD); end
MF = fullfile(OD, sprintf('wbC_%02d.mat', CI));
TF = fullfile(OD, sprintf('wbC_%02d_progress.txt', CI));

A = struct('name', CLS, 'igd', {cell(nP,1)}, 'fe', {cell(nP,1)}, ...
           'gen', {cell(nP,1)}, 'tim', {cell(nP,1)}, 'Nreal', {cell(nP,1)});
if exist(MF,'file'), S = load(MF,'A'); if isfield(S,'A'), A = S.A; end; end
logline(TF, sprintf('=== wbcat cfg=%d (%s) | %s ===', CI, CLS, datestr(now)));

for pp = 1:nP
    if numel(A.igd{pp}) ~= WNS
        A.igd{pp} = nan(1,WNS); A.fe{pp} = nan(1,WNS); A.gen{pp} = nan(1,WNS);
        A.tim{pp} = nan(1,WNS); A.Nreal{pp} = nan(1,WNS);
    end
    for ss = 1:WNS
        if ~isnan(A.igd{pp}(ss)), continue; end
        try
            rng(ss);
            F = feval(PR{pp},'M',3); F.Setting(); F.maxFE = WNFE;
            t0 = tic;
            Mth = feval(CLS, 'save',0,'outputFcn',@(a,q) []);
            Mth.Solve(F);
            Pn = Mth.result{end};
            PF = feval(PR{pp},'M',3).GetOptimum(400);
            A.igd{pp}(ss) = myIGD(Pn.objs, PF, Pn.cons);
            A.fe{pp}(ss) = F.FE; A.tim{pp}(ss) = toc(t0);
            A.Nreal{pp}(ss) = size(Pn.objs,1);
            save(MF,'A');
            logline(TF, sprintf('[%s %s s%02d] igd=%.5f fe=%d Nreal=%d tim=%.1fs', CLS, PR{pp}, ss, A.igd{pp}(ss), F.FE, size(Pn.objs,1), A.tim{pp}(ss)));
        catch e
            logline(TF, sprintf('[%s %s s%02d] FAIL: %s', CLS, PR{pp}, ss, e.message));
        end
    end
end
logline(TF, sprintf('=== DONE cfg=%d ===', CI));
disp('WBCAT_DONE');
end
function logline(f,s), fid=fopen(f,'a'); fprintf(fid,'%s\n',s); fclose(fid); end
