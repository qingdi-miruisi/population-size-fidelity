\def\sci@fileversion{3.09}
\def\sci@filedate{2025/10/27}
\def\@journal{Sci China Inf Sci}
\def\@issn{1674-733X}
\def\@copyright{\copyright~Science China Press 2026}
\def\@oacopyright{\copyright~The Author(s) 2026. This article is published with open access at \url{link.springer.com}.}
\def\@website{\url{info.scichina.com}~~~~\url{link.springer.com}}

\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{SCIS}[\sci@filedate, \sci@fileversion]

\LoadClass[twoside]{article}
%% math packages
\RequirePackage{amsmath,amsthm,amsfonts,amssymb,bm,upgreek,multicol,mathrsfs,pifont,amscd,latexsym,geometry,color,longtable}
%% graphics packages
\RequirePackage{graphicx,picins}
%% other packages
\RequirePackage{algorithm,algorithmic,tabularx,url,float,booktabs}
\RequirePackage{multirow,colortbl}
\RequirePackage{lettrine}%首字母双行
%% check pdfTeX mode
\RequirePackage{ifpdf}
\RequirePackage{fancyhdr,lastpage}
\RequirePackage[pdfstartview=FitH,colorlinks,breaklinks,linkcolor=black,citecolor=black,filecolor=black,urlcolor=black,hyperindex,CJKbookmarks]{hyperref}
\RequirePackage{breakurl}
%\RequirePackage[dvipdfm,colorlinks,linkcolor=black,citecolor=black,filecolor=black,urlcolor=black,hyperindex,CJKbookmarks]{hyperref}
\urlstyle{same}%定义url字体和正文相同
\renewcommand{\today}{\number\year-\number\month-\number\day}%日期格式

%-------------------- Page layout --------------------
\paperwidth 21 true cm                  % 纸张宽
\paperheight 28 true cm                 % 纸张高
\textwidth=176truemm
\textheight=230truemm
\topmargin=-26pt
\headsep=6truemm
\oddsidemargin=-8truemm
\evensidemargin=-8truemm
\parindent=0pt
\footskip=0mm
\renewcommand{\baselinestretch}{1.0}
\renewcommand{\arraystretch}{1.3}
\def\blank{ }
\def\lastpage{\pageref{LastPage}}
\def\firstpage{\pageref{FirstPage}}
\definecolor{sciscolor}{rgb}{0.01,0.12,0.67}
%-------------------- Font Size --------------------
\newcommand{\journalnamesize}{\fontsize{15pt}{2\baselineskip}\selectfont}
\newcommand{\titlesize}{\fontsize{16pt}{1.5\baselineskip}\selectfont}
\newcommand{\authorsize}{\fontsize{12pt}{\baselineskip}\selectfont}
\newcommand{\sectionsize}{\fontsize{12pt}{\baselineskip}\selectfont}
\newcommand{\mainbodysize}{\fontsize{10pt}{\baselineskip}\selectfont}
\newcommand{\abstractsize}{\fontsize{7pt}{0.75\baselineskip}\selectfont}
\newcommand{\shortpapersize}{\fontsize{8pt}{0.85\baselineskip}\selectfont}
\renewcommand{\footnotesize}{\fontsize{7pt}{0.75\baselineskip}\selectfont}
\newcommand{\headerfootersize}{\fontsize{7pt}{0.6\baselineskip}\selectfont}
\newcommand{\liuhao}{\fontsize{6.5pt}{0.6\baselineskip}\selectfont}

\iffalse
\makeatletter
\renewcommand\normalsize{
   \@setfontsize\normalsize\@xpt\@xiipt
   \abovedisplayskip 9\p@ \@plus4\p@ \@minus5\p@
   \abovedisplayshortskip \z@ \@plus3\p@
   \belowdisplayshortskip 6\p@ \@plus3\p@ \@minus3\p@
   \belowdisplayskip  \abovedisplayskip
   \let\@listi\@listI}
\makeatother
\fi

%-------------------- list --------------------
\renewenvironment{itemize}{
\begin{list}{$\bullet$}{
\labelwidth=4em
\labelsep=0.5em
\leftmargin=0em
\rightmargin=0em
\parsep=\parskip
\itemsep=0em
\topsep=0em
\itemindent=2.1em
}
}{\end{list}}


%-------------------- Article Type --------------------
\def\review{REVIEW}
\def\article{RESEARCH PAPER}
\def\perspective{PERSPECTIVE}
\def\moop{MOOP}
\def\news{NEWS \& VIEWS}
\def\highlight{HIGHLIGHT}
\def\letter{LETTER}
\def\erratum{ERRATUM}
\def\editorial{EDITORIAL}
\def\supplementary{Supplementary File}

%-------------------- Article Information --------------------
\let\@ArticleType\@empty \def\ArticleType#1{\def\@ArticleType{#1}}
\let\@SpecialTopic\@empty \def\SpecialTopic#1{\def\@SpecialTopic{#1}}
\let\@SpecialTopics\@empty \def\SpecialTopics#1{\def\@SpecialTopics{#1}}
\let\@Year\@empty \def\Year#1{\def\@Year{#1}}
\let\@Month\@empty \def\Month#1{\def\@Month{#1}}
\let\@Vol\@empty \def\Vol#1{\def\@Vol{#1}}
\let\@No\@empty \def\No#1{\def\@No{#1}}
\let\@AuthorMark\@empty \def\AuthorMark#1{\def\@AuthorMark{#1}}
\let\@AuthorCitation\@empty \def\AuthorCitation#1{\def\@AuthorCitation{#1}}
\let\@BeginPage\@empty \def\BeginPage#1{\def\@BeginPage{#1}}
\let\@EndPage\@empty \def\EndPage#1{\def\@EndPage{#1}}
\let\@DOI\@empty \def\DOI#1{\def\@DOI{#1}}
\let\@ArtNo\@empty \def\ArtNo#1{\def\@ArtNo{#1}}
\let\@ReceiveDate\@empty \def\ReceiveDate#1{\def\@ReceiveDate{#1}}
\let\@ReviseDate\@empty \def\ReviseDate#1{\def\@ReviseDate{#1}}
\let\@AcceptDate\@empty \def\AcceptDate#1{\def\@AcceptDate{#1}}
\let\@OnlineDate\@empty \def\OnlineDate#1{\def\@OnlineDate{#1}}
\let\@abstract\@empty \renewcommand\abstract[1]{\def\@abstract{#1}}
\let\@keywords\@empty \def\keywords#1{\def\@keywords{#1}}
\let\@contributions\@empty \newcommand\contributions[1]{\def\@contributions{#1}}
\let\@luntan\@empty \newcommand\luntan{\def\@luntan{1}}
\let\@oatag\@empty \newcommand\oa{\def\@oatag{1}}

%-------------------- Citation --------------------
\def\citationline{
\ifx\@DOI\@empty \@titlecitation. \@journal, for review
\else \@AuthorCitation. \@titlecitation. \@journal, \@Year, \@Vol(\@No): \@ArtNo, \href{https://doi.org/\@DOI}{\url{https://doi.org/\@DOI}}
\fi}

%-------------------- Title --------------------
\let\@title\@empty
\renewcommand\title[3][]{
  \def\@title{#2}
  \def\@titlehead{#1}
  \def\@titlecitation{#3}
  \ifx\@titlehead\@empty \def\@titlehead{#2}\fi
  \ifx\@titlecitation\@empty \def\@titlecitation{#2}\fi
}

%-------------------- Author --------------------
\let\@author\@empty
\let\@authoremail\@empty
\let\@onlyoneauthor\@empty
\renewcommand*{\author}[3][]{
  \ifx\@author\@empty
    \def\@author{#2\@authornote{#1}{#3}}
    \let\@authortemp\@author
  \else
    \let\@author\@authortemp
    \def\@onlyoneauthor{No}
    \expandafter\def\expandafter\@author\expandafter
      {\@author~{\&}~#2\@authornote{#1}{#3}}
    \expandafter\def\expandafter\@authortemp\expandafter
      {\@authortemp,~#2\@authornote{#1}{#3}}
  \fi

  %联系作者邮箱
  \ifx#3\@empty
  \else
      \ifx\@authoremail\@empty \def\@authoremail{#3}
      \else \expandafter\def\expandafter\@authoremail\expandafter{\@authoremail, #3}
      \fi
  \fi
}

\def\@authornote#1#2{%
  \def\SCAE@author@address{#1}%
  \def\SCAE@author@footnote{#2}%

  \ifx\SCAE@author@address\@empty
  \else \textsuperscript{#1}%\hspace{-1.4mm}
  \fi

  \ifx\SCAE@author@footnote\@empty
  \else \ifx\@onlyoneauthor\@empty \textsuperscript{*}%\hspace{-1.4mm}
  \else \ifx\@contributions\@empty \textsuperscript{*}%\hspace{-1.4mm}
  \fi\fi\fi
}

%-------------------- Address --------------------
\def\@address{}
\newcommand*{\address}[2][]{
  \ifx\@address\@empty \def\@address{\@addressline{#1}{#2}}
  \else \expandafter\def\expandafter\@address\expandafter{\@address\tabularnewline\@addressline{#1}{#2}}
  \fi}
\def\@addressline#1#2{\@addresscr\hb@xt@1ex{\textsuperscript{\rm#1}\hss}#2}
\def\@addresscr{\def\\{\tabularnewline\@addresscr\hbox to1ex{}\ignorespaces}}


%-------------------- maketitle --------------------
\renewcommand\maketitle{\par
  \begingroup
    \renewcommand\thefootnote{\fnsymbol{footnote}}
    \let\footnote\thanks
    \def\@makefnmark{\hbox{\@textsuperscript{\normalfont\@thefnmark}}}%
    \long\def\@makefntext##1{\noindent\@textsuperscript{\normalfont\@thefnmark}##1}%
    \@maketitle
    \thispagestyle{empty}\@thanks
    \long\def\@makefntext##1{\noindent##1}
  \endgroup
  \renewcommand\thefootnote{\arabic{footnote}}
  \setcounter{footnote}{0}
  \setlength{\textheight}{23.6cm}
  \parindent=10.8pt
  \baselineskip 12pt
  %字号:moop,perspective,news,highlight,letter字号小
  \ifx\@ArticleType\moop \shortpapersize
  \else \ifx\@ArticleType\perspective \shortpapersize
  \else \ifx\@ArticleType\news \shortpapersize
  \else \ifx\@ArticleType\highlight \shortpapersize
  \else \ifx\@ArticleType\letter \shortpapersize
  \else \mainbodysize
  \fi\fi\fi\fi\fi
  
}

\long\def\@makefntext#1{\parindent 12pt \indent\hbox{\hss{\@thefnmark)\ }}#1}
\def\@makefnmark{\hbox\textsuperscript{\@thefnmark)}}


\def\@maketitle{
    \ifthenelse{\pageref{LastPage}=1}
        {\def\@pagerank{\@ArtNo}}
        {\def\@pagerank{\@ArtNo:1--\@ArtNo:\pageref{LastPage}}}

    %首页页眉页脚
    \begin{picture}(0,0)
        \put(185,23){\journalnamesize\bf \textcolor[rgb]{0.01,0.12,0.67}{SCIENCE CHINA}}
        \put(187,8){\journalnamesize \textcolor[rgb]{0.01,0.12,0.67}{Information Sciences}}
        %\put(0,1){\thicklines\line(1,0){456}}
        \put(0,0){\color[rgb]{0.01,0.12,0.67}{\rule{\linewidth}{0.5pt}}}
        \ifx\@DOI\@empty\else
            \put(0,7){\makebox[\textwidth][r]{\href{http://crossmark.crossref.org/dialog/?doi=\@DOI&domain=pdf&date_stamp=\today}{\includegraphics{Print-CrossMark.eps}}}}
            \put(0,-9){\makebox[\textwidth][r]{\vbox{\hbox{\headerfootersize \@Month~\@Year,~Vol.~\@Vol,~Iss.~\@No,~\@pagerank}}}}
            \put(0,-18){\makebox[\textwidth][r]{\vbox{\hbox{\headerfootersize \href{https://doi.org/\@DOI}{https://doi.org/\@DOI}}}}}
            \ifx\@luntan\@empty\else \put(0,-90){\makebox[\textwidth][r]{\includegraphics{kxqylt.eps}}} \fi
            \ifx\@oatag\@empty \put(0,-660){\makebox[\textwidth][l]{\headerfootersize\sf \@copyright}}
            \else \put(0,-660){\makebox[\textwidth][l]{\headerfootersize\sf \@oacopyright}}
            \fi
            \put(0,-660){\makebox[\textwidth][r]{\headerfootersize\sf \@website}}
        \fi
    \end{picture}
    
    %首页页眉下方左侧:editorial不写专题名
    \begin{picture}(0,0)
    \rm
    \put(0,-5){\makebox[\textwidth][l]{\bf \textcolor[rgb]{0.01,0.12,0.67}{{\LARGE\bfseries\raisebox{2pt}{.}}~\@ArticleType~{\LARGE\bfseries\raisebox{2pt}{.}}}}}
    \ifx\@ArticleType\editorial\else \put(1,-32){\@SpecialTopic} \fi
    \ifx\@ArticleType\editorial\else \put(1,-20){\@SpecialTopics} \fi
    \end{picture}
    
    %标题:editorial标题下方有空行
    \noindent
    \vskip 12mm
    \begin{center}\titlesize\bfseries\@title\end{center}

    %作者和单位:editorial没有
    \ifx\@ArticleType\editorial\else
      \begin{center}\authorsize{\rm
          \begin{tabular}{@{}c@{}}
          \@author
          \ifx\@onlyoneauthor\@empty
            \setcounter{footnote}{-1}
            \footnote{*{\thinspace}Corresponding author (email:~\@authoremail)}
          \else
            \ifx\@contributions\@empty
                \setcounter{footnote}{-1}
                \footnote{*{\thinspace}Corresponding author (email:~\@authoremail)}
            \else
                \setcounter{footnote}{-1}
                \footnote{*{\thinspace}Corresponding author (email:~\@authoremail)\protect\\\dag{\thinspace}\@contributions}
            \fi
          \fi
          \end{tabular}
      }\end{center}
      \begin{center}\headerfootersize{\it \begin{tabular}[t]{@{}c@{}} \@address \end{tabular}} \end{center}
  \fi

%投稿日期:erratum,editorial,supplementary没有
\ifx\@ArticleType\erratum\else
\ifx\@ArticleType\editorial\else
\ifx\@ArticleType\supplementary\else
      \begin{center}
          \footnotesize
          \ifx\@DOI\@empty
          \else \ifx\@ReviseDate\@empty
              \ifx\@OnlineDate\@empty{Received \@ReceiveDate/Accepted \@AcceptDate}
              \else{Received \@ReceiveDate/Accepted \@AcceptDate/Published online \@OnlineDate}
              \fi
          \else
              \ifx\@OnlineDate\@empty{Received \@ReceiveDate/Revised \@ReviseDate/Accepted \@AcceptDate}
              \else{Received \@ReceiveDate/Revised \@ReviseDate/Accepted \@AcceptDate/Published online \@OnlineDate}
              \fi
          \fi\fi
      \end{center}
      \begin{center}
      %\vskip -10mm
          \begin{tabular}{p{0.95\textwidth}}
          \arrayrulecolor{sciscolor}
          %\color[rgb]{0.01,0.12,0.67}{\rule{\linewidth}{0.5pt}}
          \toprule
              %摘要和关键词:moop,perspective,news,highlight,letter没有
              \ifx\@ArticleType\moop
              \else \ifx\@ArticleType\perspective
              \else \ifx\@ArticleType\news
              \else \ifx\@ArticleType\highlight
              \else \ifx\@ArticleType\letter
              \else
                \abstractsize\noindent\textcolor{black}{\textbf{Abstract}\quad\ignorespaces\@abstract}\\
                \abstractsize\noindent\textcolor{black}{\textbf{Keywords}\quad\ignorespaces\@keywords}\\
                \hline
                %\vskip -7mm
               % \color[rgb]{0.01,0.12,0.67}{\rule{\linewidth}{0.5pt}}
              \fi\fi\fi\fi\fi
              \abstractsize\noindent\textcolor{black}{\textbf{Citation}\quad\ignorespaces\citationline}\\
\bottomrule
          %\vskip -7mm
         % \color[rgb]{0.01,0.12,0.67}{\rule{\linewidth}{0.5pt}}
          \end{tabular}
         % \vskip -4mm
      \end{center}
%\vskip -4mm
\fi\fi\fi
}


%-------------------- Running heads --------------------
\pagestyle{fancy}
\lhead{}
\chead{\headerfootersize
        \ifx\@DOI\@empty \emph{\@journal}\ \ \ \thepage
        \else
            \ifx \@onlyoneauthor\@empty
                \@AuthorMark\ \ \ \emph{\@journal}\ \ \ \@Month~\@Year,~Vol.~\@Vol,~Iss.~\@No,~\@ArtNo:\thepage
            \else
                \@AuthorMark\emph{,~et al.\ \ \ \@journal}\ \ \ \@Month~\@Year,~Vol.~\@Vol,~Iss.~\@No,~\@ArtNo:\thepage
            \fi
        \fi}
\rhead{}
\lfoot{}
\cfoot{}
\rfoot{}
\renewcommand{\headrulewidth}{0.0pt}%改为0pt即可去掉页眉下面的横线
\renewcommand{\footrulewidth}{0.0pt}%改为0pt即可去掉页脚上面的横线


%-------------------- Acknowledgements --------------------
\newcommand\Acknowledgements[1]{
    \vspace*{2mm}
    \begin{itemize}\footnotesize
        \item[] \noindent\textbf{Acknowledgements}\quad #1
    \end{itemize}
}

\newcommand\Supplements[1]{
    \vspace*{2mm}
    \begin{itemize}\footnotesize
        \item[] \noindent\textbf{Supporting information}\quad #1\quad
        The supporting information is available online at \url{info.scichina.com} and \url{link.springer.com}.
        The supporting materials are published as submitted, without typesetting or editing.
        The responsibility for scientific accuracy and content remains entirely with the authors.
    \end{itemize}
}

\newcommand\FundingNote[1]{
    \vspace*{2mm}
    \begin{itemize}\footnotesize
        \item[] \noindent#1
    \end{itemize}
}

%-------------------- Sections --------------------
\renewcommand\section{
    \@startsection{section}{1}{\z@}%
    {-4.5ex \@plus -1ex \@minus -.2ex}%
    {2.5ex \@plus.1ex}%
    {\normalfont\sectionsize\bfseries}}

\renewcommand\subsection{
    \@startsection{subsection}{2}{\z@}%
    {-2ex\@plus -2ex \@minus -.1ex}%
    {2ex \@plus .2ex}%
    {\normalfont\normalsize\bfseries}}

\renewcommand\subsubsection[1]{
    \@startsection{subsubsection}{3}{\z@}%
    {-3ex\@plus -1ex \@minus -.1ex}%
    {1ex \@plus .1ex}%
    {\normalfont\normalsize}{\it#1}}

\newcommand\deareditor{
    \noindent Dear editor,\vspace{1mm}\\
    \noindent
}

\newcommand\lettersection[1]{{\it #1}.}
\columnsep 0.5cm  %两栏之间的距离

\let\oldappendix\appendix
\renewenvironment{appendix}{
    \oldappendix
    \setcounter{section}{0}
    \def\thesection{Appendix \Alph{section}}
    \renewcommand{\theequation}{\Alph{section}\arabic{equation}}
    \renewcommand{\thefigure}{\Alph{section}\arabic{figure}}
    \renewcommand{\thetable}{\Alph{section}\arabic{table}}
    \renewcommand{\thealgorithm}{\Alph{section}\arabic{algorithm}}
    \renewcommand{\theproposition}{\Alph{section}\arabic{proposition}}
    \renewcommand{\thelemma}{\Alph{section}\arabic{lemma}}
      \renewcommand{\thetheorem}{\Alph{section}\arabic{theorem}}
    \renewcommand{\section}{
        \setcounter{equation}{0}
        \setcounter{table}{0}
        \setcounter{figure}{0}
        \setcounter{algorithm}{0}
        \setcounter{proposition}{0}
        \setcounter{lemma}{0}
        \@startsection{section}{1}{\z@}%
        {-4.5ex \@plus -1ex \@minus -.2ex}%
        {1ex \@plus .2ex}%
        {\normalfont\normalsize\bfseries}
    }
    \shortpapersize
}


\newenvironment{profile}{
    \newpage
    \def\thesection{}
    \def\thesubsection{}
    \renewcommand{\section}{
        \@startsection{section}{1}{\z@}%
        {5ex \@plus -1ex \@minus -.2ex}%
        {5ex \@plus .2ex}%
        {\centering\normalfont\sectionsize\bfseries}
    }
    \renewcommand{\subsection}{
        \@startsection{subsection}{2}{-2.5ex}%
        {-2ex\@plus -2ex \@minus -.1ex}%
        {2ex \@plus .2ex}%
        {\normalfont\sectionsize\bfseries}
    }
    \abstractsize
}

%-------------------- Bibliography --------------------
\usepackage{cite}%使多个参文中间用--连接
\def\@biblabel#1{#1~}
\renewenvironment{thebibliography}[1]{
    %双栏参文行距需要调整
    \ifx\@ArticleType\moop \renewcommand{\baselinestretch}{1.2}
    \else \ifx\@ArticleType\perspective \renewcommand{\baselinestretch}{1.2}
    \else \ifx\@ArticleType\news \renewcommand{\baselinestretch}{1.2}
    \else \ifx\@ArticleType\highlight \renewcommand{\baselinestretch}{1.2}
    \else \ifx\@ArticleType\letter \renewcommand{\baselinestretch}{1.2}
    \fi\fi\fi\fi\fi
    
    \ifx\@oatag\@empty\else
        \vspace*{2mm}
        \begin{itemize}\footnotesize
        \item[] \noindent\textbf{Open Access}\quad
        This article is licensed under a Creative Commons Attribution 4.0 International License, 
        which permits use, sharing, adaptation, distribution and reproduction in any medium or format, 
        as long as you give appropriate credit to the original author(s) and the source, 
        provide a link to the Creative Commons licence, and indicate if changes were made. 
        The images or other third party material in this article are included in the article's Creative Commons licence, 
        unless indicated otherwise in a credit line to the material. 
        If material is not included in the article's Creative Commons licence and 
        your intended use is not permitted by statutory regulation or exceeds the permitted use, 
        you will need to obtain permission directly from the copyright holder.
        To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by/4.0/}.
        \end{itemize}
    \fi
    
    
    \vspace*{-4mm}
    \section*{\footnotesize\refname
              \@mkboth{\footnotesize\refname}{\footnotesize\refname}}
    \vspace*{-3mm}
    \list{\@biblabel{\@arabic\c@enumiv}}{
        \settowidth\labelwidth{\@biblabel{#1}}
        \leftmargin\labelwidth
        \advance\leftmargin\labelsep
        \@openbib@code
        \usecounter{enumiv}
        \let\p@enumiv\@empty
        \renewcommand\theenumiv{\@arabic\c@enumiv}
        \renewcommand{\baselinestretch}{1.1}
        \footnotesize
    }
    \itemsep 0ex \parskip 0ex
    \footnotesize\sloppy
    
}
\renewcommand{\UrlFont}{\selectfont} %使用\url{}使参文中的url自动断行




%-------------------- Figure and table --------------------
\setlength{\floatsep}{12pt plus 2pt minus 2pt}%页面顶部/底部的浮动对象间的垂直距离, 缺省为12pt plus 2pt minus 2pt
\setlength{\textfloatsep}{12pt plus 2pt minus 2pt}%页顶部/底部的浮动对象与文本间垂直距离, 缺省12pt plus 2pt minus 2pt
\setlength{\intextsep}{12pt plus 2pt minus 2pt}%页中浮动对象与上下方文本间垂直距离, 缺省12pt plus 2pt minus 2pt
\setlength{\belowrulesep}{1pt}%横线和其下文字的间距
\setlength{\aboverulesep}{1pt}%横线和其上文字的间距
\setlength{\doublerulesep}{0.4pt}
\newcommand\Times{\fontfamily{ptm}\selectfont}
\newcommand{\picsize}{\fontsize{8pt}{0.4\baselineskip}\selectfont}
\usepackage[bf,footnotesize,labelsep=quad]{caption}
\usepackage[labelfont={rm,md,up}]{subfig}
\captionsetup[subfloat]{labelformat=simple,captionskip=0pt}
\captionsetup[table]{aboveskip=1mm}
\captionsetup[figure]{aboveskip=3mm}
\captionsetup[algorithm]{font=footnotesize}
\renewcommand{\thesubfigure}{{\picsize\Times(\alph{subfigure})}} %这两行定义子图在正文引用时的label形式
\renewcommand{\thesubtable}{{\picsize(\alph{subtable})}} %子表label的字体仍和正文相同

%-------------------- Math --------------------
\def\leq{\leqslant}
\def\geq{\geqslant}
\def\le{\leqslant}
\def\ge{\geqslant}
\abovedisplayskip=11pt plus 0pt minus 6pt
\belowdisplayskip=11pt plus 0pt minus 6pt
\newcommand{\set}[1]{\ensuremath{\left\{ #1 \right\}}}%
\newcommand{\Set}[2]{\ensuremath{\left\{ #1 \left| \right. #2 \right\}}}%
\newcommand{\abs}[1]{\ensuremath{\left| #1 \right|}}%
\newcommand{\map}[3]{\ensuremath{#1 : #2 \rightarrow #3}}%
\newcommand{\C}[1]{\ensuremath{\mathcal{#1}}}%
\newcommand{\restrict}[2]{\ensuremath{#1 \left|_{#2}\right.}}%
\newcommand{\NN}{\mathbb{N}^0}
\newcommand{\PN}{\mathbb{N}}
\newcommand{\syn}{\mathbf{S}}
\newcommand{\Syn}{\mathbf{M}}
\allowdisplaybreaks
\setlength{\arraycolsep}{2.0pt}

%-------------------- Theorem --------------------
\def\proof{\noindent{\it Proof.}\quad}
\def\th#1{\noindent{\bf #1}\quad}%The common style. 通用形式
\renewcommand{\qedsymbol}{}
\newtheoremstyle{newdefinition}%
    {2pt}% Space above
    {2pt}% Space below
    {\normalfont}% Body font
    {}% Indent amount
    {\bfseries}% Theorem head font
    {.}% Punctuation after theorem head
    {10pt plus 1pt minus 1pt}% Space after theorem head
    {}% Theorem head spec (can be left empty, meaning `normal')
\theoremstyle{newdefinition}
\newtheorem{assumption}{Assumption}
\newtheorem{corollary}{Corollary}
\newtheorem{definition}{Definition}
\newtheorem{example}{Example}
\newtheorem{lemma}{Lemma}
\newtheorem{problem}{Problem}
\newtheorem{proposition}{Proposition}
\newtheorem{remark}{Remark}
\newtheorem{theorem}{Theorem}


\endinput
