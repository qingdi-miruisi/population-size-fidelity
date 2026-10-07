function audit13(mode)
% audit13 -- round-13 verified audit of the PlatEMO algorithm tree.
%
%   audit13('ast')   static classification of every affected file using the
%                    MATLAB parser (mtree), so that matches inside comments and
%                    string literals cannot occur. Reports, per file, the line
%                    of the constructor assignment, the line of the population
%                    initialisation, and their order.
%   audit13('dyn')   dynamic three-quantity probe: for each standalone
%                    reference-vector algorithm, configure N=100, run it, and
%                    record N_req (configured), N_real (population actually
%                    evaluated) and N_rep (what the framework's own result
%                    table displays afterwards).
%
%   Output: D:\wb_run3\audit13_<mode>.txt  and  ..._<mode>.csv

BASE = 'D:\harness工作\中国科学：数学(总)\算法\algorithm';
TREE = fullfile(BASE, '_tmp_official\PlatEMO-master\PlatEMO');
OUT  = 'D:\wb_run3';
if nargin < 1, mode = 'ast'; end

if strcmp(mode,'ast')
    ast_pass(TREE, OUT);
else
    dyn_pass(TREE);
end
end

% ===================================================================== static
function ast_pass(TREE, OUT)
ALGDIR = fullfile(TREE, 'Algorithms');
files  = dir(fullfile(ALGDIR, '**', '*.m'));
pat    = 'Problem\.N\]\s*=\s*UniformPoint\(Problem\.N';

fid = fopen(fullfile(OUT,'audit13_ast.csv'),'w');
fprintf(fid,'algorithm,file,assign_line,assign_text,init_line,order,uses_Z_after\n');

n = 0; nLive = 0; nBefore = 0; nAfter = 0; nNoInit = 0;
for k = 1 : numel(files)
    f = fullfile(files(k).folder, files(k).name);
    try
        t = mtree(f, '-file');
        % positions of every statement, with the comment/string structure
        % already resolved by the parser
        aLine = []; aTxt = '';
        iLine = [];
        for node = t.nodes
            [kind, txt] = nodekind(node);
            if strcmp(kind,'CALL') || strcmp(kind,'EQUALS') || strcmp(kind,'EXPR')
                if ~isempty(regexp(txt, pat, 'once'))
                    aLine = node.lineno; aTxt = strtrim(txt);
                end
                if isempty(iLine) && ~isempty(regexp(txt, '\.Initialization\s*\(', 'once'))
                    iLine = node.lineno;
                end
            end
        end
        if isempty(aLine), continue; end
        n = n + 1; nLive = nLive + 1;
        rel = strrep(strrep(f, [ALGDIR filesep], ''), '\', '/');
        parts = strsplit(rel,'/');
        alg = parts{min(2,numel(parts))};
        if isempty(iLine)
            order = 'no-init-in-file'; nNoInit = nNoInit + 1;
        elseif aLine < iLine
            order = 'assign-before-init'; nBefore = nBefore + 1;
        else
            order = 'assign-AFTER-init'; nAfter = nAfter + 1;
        end
        src = fileread(f);
        ls  = strsplit(src, newline);
        usesZ = 0;
        if aLine < numel(ls)
            tail = strjoin(ls(aLine+1:end), ' ');
            usesZ = ~isempty(regexp(tail, '\bZ\b', 'once'));
        end
        txt = regexprep(aTxt, '[\r\n]+', ' ');
        txt = strrep(txt, ',', ';');
        fprintf(fid,'%s,%s,%d,"%s",%d,%s,%d\n', alg, rel, aLine, txt, iLine, order, usesZ);
    catch
        % parser failure: record and continue
        fprintf(fid,'%s,%s,-1,"PARSE-FAIL",-1,parse-fail,0\n', '', files(k).name);
    end
end
fclose(fid);

fid = fopen(fullfile(OUT,'audit13_ast.txt'),'w');
fprintf(fid,'AST audit of the PlatEMO 4.16 algorithm tree (MATLAB mtree parser)\n');
fprintf(fid,'files scanned                     : %d\n', numel(files));
fprintf(fid,'files with a live constructor call: %d\n', nLive);
fprintf(fid,'  assignment BEFORE Initialization: %d\n', nBefore);
fprintf(fid,'  assignment AFTER  Initialization: %d\n', nAfter);
fprintf(fid,'  no Initialization in the file   : %d\n', nNoInit);
fprintf(fid,'per-file detail: audit13_ast.csv\n');
fclose(fid);
disp('AST_DONE');
end

function [kind, txt] = nodekind(node)
try
    kind = node.kind;
catch
    kind = '';
end
try
    txt = node.string;
catch
    txt = '';
end
if iscell(txt), txt = strjoin(txt,' '); end
end

% ==================================================================== dynamic
function dyn_pass(TREE)
addpath(genpath(fullfile(TREE,'Algorithms')));
addpath(genpath(fullfile(TREE,'Problems')));
addpath(genpath(fullfile(TREE,'Metrics')));
warning('off','all');

algs = {'NSGAIII','MOEAD','RVEA','LMOCSO','FDSEA','HEA','CTAEA','NSGAII', ...
        'MOEADDRA','MOEADDE','RVEAa','DGEA','PPS','SPEA2','IBEA','MOEADSTM'};
fid = fopen('D:\wb_run3\audit13_dyn.csv','w');
fprintf(fid,'algorithm,N_req,UniformPoint_returned,N_real,fe,Problem_N_after\n');
for a = 1 : numel(algs)
    aname = algs{a};
    try
        Pro = DTLZ2('N',100,'M',3,'D',30,'maxFE',1000);
        nreq = Pro.N;
        [~,nret] = UniformPoint(nreq, 3);
        Al = feval(aname,'save',0);
        Al.Solve(Pro);
        S = Al.result{end,2};
        nreal = numel(S);
        fe = Pro.FE;
        fprintf(fid,'%s,%d,%d,%d,%d,%d\n', aname, nreq, nret, nreal, fe, Pro.N);
        fprintf('%-12s N_req=%d UniformPoint->%d N_real=%d Problem.N_after=%d\n', ...
                aname, nreq, nret, nreal, Pro.N);
    catch ME
        fprintf(fid,'%s,%d,,,,\n', aname, 100);
        fprintf('%-12s FAILED: %s\n', aname, ME.message);
    end
end
fclose(fid);
disp('DYN_DONE');
end
