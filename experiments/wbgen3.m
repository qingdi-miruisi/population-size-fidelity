function wbgen3()
% wbgen3 - generation counts and wall clock for the published host
% (replica FDSEA_cfg with Nmode=1, bit-identical to the unmodified file) and
% for the corrected host (Nmode=0).  5 seeds per problem.
cd('D:\harness工作\中国科学：数学(总)\算法\algorithm');
P = '_tmp_official/PlatEMO-master/PlatEMO';
p = strsplit(path,';'); keep = ~contains(p,'Huawei_Cup','IgnoreCase',true); path(strjoin(p(keep),';'));
addpath(genpath([P '/Algorithms'])); addpath(genpath([P '/Problems'])); addpath(genpath([P '/Metrics']));
addpath('algorithms'); addpath('algorithms/FDSEA'); addpath('D:\wb_run');
warning('off','all'); set(0,'DefaultFigureVisible','off');

PR = { {'DTLZ1',3,300}, {'DTLZ2',3,300}, {'DTLZ7',3,300}, ...
       {'LSMOP1',3,300}, {'LSMOP2',3,300}, {'LSMOP3',3,300}, {'LSMOP4',3,300}, ...
       {'LSMOP5',3,300}, {'LSMOP6',3,300}, {'LSMOP7',3,300}, {'LSMOP8',3,300}, {'LSMOP9',3,300} };
nP = numel(PR); NS = 5; WNFE = 100000;
OD = 'results/wbgen3'; if ~exist(OD,'dir'), mkdir(OD); end
MF = fullfile(OD,'wbG.mat'); TF = fullfile(OD,'wbG_progress.txt');
R = struct('fe', nan(2,nP,NS), 'gen', nan(2,nP,NS), 'tim', nan(2,nP,NS), 'igd', nan(2,nP,NS));
if exist(MF,'file'), S=load(MF,'R'); if isfield(S,'R'), R=S.R; end; end
logline(TF, sprintf('=== wbgen3 | %s ===', datestr(now)));
for mode = 0:1            % 0 = corrected host, 1 = published host
    for pp = 1:nP
        for ss = 1:NS
            if ~isnan(R.igd(mode+1,pp,ss)), continue; end
            try
                rng(ss);
                F = feval(PR{pp}{1},'M',PR{pp}{2},'D',PR{pp}{3}); F.Setting(); F.maxFE = WNFE;
                t0 = tic;
                A = FDSEA_cfg('save',0,'outputFcn',@(a,q) []);
                A.nexch = 10; A.gama = 0; A.K0 = 5; A.Nmode = mode; A.refmode = 0; A.rec = 1;
                A.Solve(F);
                R.fe(mode+1,pp,ss) = F.FE; R.gen(mode+1,pp,ss) = A.hist.generations;
                R.tim(mode+1,pp,ss) = toc(t0);
                R.igd(mode+1,pp,ss) = myIGD(A.result{end}.objs, ...
                    feval(PR{pp}{1},'M',PR{pp}{2},'D',PR{pp}{3}).GetOptimum(400), A.result{end}.cons);
                save(MF,'R');
                logline(TF, sprintf('[mode%d %s s%d] gen=%.0f fe=%.0f igd=%.5f tim=%.1fs', ...
                        mode, PR{pp}{1}, ss, R.gen(mode+1,pp,ss), R.fe(mode+1,pp,ss), R.igd(mode+1,pp,ss), R.tim(mode+1,pp,ss)));
            catch e
                logline(TF, sprintf('[mode%d %s s%d] FAIL: %s', mode, PR{pp}{1}, ss, e.message));
            end
        end
    end
end
disp('WBGEN3_DONE');
end
function logline(f,s), fid=fopen(f,'a'); fprintf(fid,'%s\n',s); fclose(fid); end
