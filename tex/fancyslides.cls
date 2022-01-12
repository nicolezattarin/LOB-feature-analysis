\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{fancyslides}[2013/04/23 my custom beamer slides class]

\LoadClass{beamer}


%%%% this is a~custom class for preparing presentations
%%%% contact me if anything goes wrong
%%%% or you want to contribute to the work
%%%% pawel.lupkowski@gmail.com
%%%% release: 24.05.2013






%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% PACKAGES %%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


\RequirePackage{framed}    %% FOR FRAMED SLOGANS
\RequirePackage{tikz}      %% FOR POINTED SLOGANS


%%% redefines points for itemize
\setbeamertemplate{itemize items}{$\bullet$}
\newcommand{\fitem}[1]{$\bullet$~#1\newline}
\newcommand{\pitem}[1]{$\bullet$~#1\newline \pause}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% FRAMES FOR SLOGANS %%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newenvironment{mybox}{%
  \def\FrameCommand{\fboxsep=1cm \colorbox{\strcolor}}%
  \MakeFramed {\FrameRestore}}%
 {\endMakeFramed}


\newenvironment{mybox2}{%
  \def\FrameCommand{\fboxsep=1cm \colorbox{white}}%
  \color{black}\MakeFramed {\FrameRestore}}%
 {\endMakeFramed}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% COLOURS            %%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\definecolor{white}{rgb}{1,1,1}
\definecolor{black}{rgb}{0,0,0}
\definecolor{gray}{rgb}{0.90196079, 0.90196079, 0.90196079}
\definecolor{blue}{rgb}{0.12941177, 0.45882353, 0.60784316}
\definecolor{green}{rgb}{0.44313726 0.78431374 0.21568628}
\definecolor{orange}{rgb}{1 0.49803922 0.16470589}



\newcommand{\customtextcol}[1]{#1} %text inside boxes and dots

\newcommand{\slogan}[1]{\Huge \MakeUppercase{#1}} %text inside boxes and dots
\newcommand{\fbckg}[1]{\usebackgroundtemplate{\includegraphics[width=\paperwidth]{#1}}}%frame background

\newcommand{\thankyou}{\pointedsl{thank you}} %% thank you slide

%%% defines pointed slogan
\newcommand{\pointedsl}[1]{
\pgfsetfillopacity{\structureopacity}
\begin{center}
\tikz{ \fill[\strcolor] (0,0) circle (20ex);
\pgfsetfillopacity{1}
\node at (0,0) {
{\slogan{#1}}
};
}%%
\end{center}
}


%%% defines framed slogan
\newcommand{\framedsl}[1]{
\pgfsetfillopacity{\structureopacity}
  \begin{mybox}
\pgfsetfillopacity{1}
\begin{center}
  {\slogan{#1}}
\end{center}
\end{mybox}
}



%%% itemised list frame
\newcommand{\itemized}[1]{
\pgfsetfillopacity{\structureopacity}
  \begin{mybox}
\pgfsetfillopacity{1}
\begin{Large}
\begin{itemize}
\centering
\pgfsetfillopacity{1}
#1
\end{itemize}
\end{Large}
\end{mybox}
}




%%% starting slide
\newcommand{\startingslide}[1]{
\begin{frame}
\pgfsetfillopacity{\structureopacity}
  \begin{mybox}
\pgfsetfillopacity{1}
\begin{center}
{\Huge \titlephrase
   
}
    
\end{center}
\end{mybox}

\vspace{-1.5cm}

\pgfsetfillopacity{0.60}
\begin{mybox2}
\pgfsetfillopacity{0.80}
\name \ $\bullet$ \  \affil \ $\bullet$ \ \email
\end{mybox2}
\end{frame}
}




%%% misc slide: for putting different stuff into it
\newcommand{\misc}[1]{
\pgfsetfillopacity{\structureopacity}
  \begin{mybox}
\pgfsetfillopacity{1}
\begin{center}
#1
\end{center}
\end{mybox}
}


%%% sources slide
\newcommand{\sources}[1]{
\pgfsetfillopacity{\structureopacity}
\begin{mybox}
\begin{block}{{\Huge \bf SOURCES}}
\pgfsetfillopacity{1}
~\\
#1
\end{block}
\end{mybox}  
}



\endinput