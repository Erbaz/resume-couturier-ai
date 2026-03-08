templates = [
    {
        'id': '1',
        'name': 'template 1',
        'thumbnail': r'server/assets/resume_thumbnail_id_1.jpeg',
        'latex':
        r"""
                    %------------------------
            % Latex CV Template for COS Northeastern University Faculty
            % Author: Zoe Kearney

            % Formatting: https://www.overleaf.com/latex/templates/coles-resume-template/qhpynjcvjpcj

            % Follows: Template Dossier Documents, Office of the Provost, Northeastern; July 1, 2025 version (https://provost.northeastern.edu/faculty-affairs/). 

            %Disclaimer: This template is intended to complement Northeastern University’s dossier guidelines for tenure and promotion cases, as well as discipline-specific CV standards.

            % License: LaTeX Project Public License 1.3c
            %------------------------

            % Document class and font size
            \documentclass[a4paper,9pt]{extarticle}

            % Packages
            \usepackage[utf8]{inputenc} % For input encoding
            \usepackage{geometry} % For page margins
            \geometry{a4paper, margin=1in} % Set paper size and margins
            \usepackage{titlesec} % For section title formatting
            \usepackage{enumitem} % For itemized list formatting
            \usepackage{hyperref} % For hyperlinks
            \usepackage{lipsum} % For filler text
            \usepackage{changepage} %For Indenting

            % Formatting
            \setlist{noitemsep} % Removes item separation
            \titleformat{\section}{\large\bfseries}{\thesection}{1em}{}[\titlerule] % Section title format
            \titlespacing*{\section}{0pt}{\baselineskip}{\baselineskip} % Section title spacing
            \newenvironment{subs} %Indenting
            {\adjustwidth{2em}{0pt}}
            {\endadjustwidth}

            %-------------------------------------------------------------------------------
            %-------------------------------------------------------------------------------
            % Begin document
            \begin{document}

            % Disable page numbers
            \pagestyle{empty}

            % Header
            \begin{center}
                \textbf{\Large LOREM IPSUM }\\[3pt] % Name
                \textbf{Curriculum Vitae}\\[1pt] % CV
                City, State | \href{mailto:example@example.com}{example@example.com} | \href{https://www.linkedin.com/in/loremipsum}{Website or LinkedIn} % Contact info
            \end{center}

            %------------------------
            % Education and Employment Section
            \section*{EDUCATION \& EMPLOYMENT HISTORY}
                \noindent
                \newline
                \textbf{Degree Name} \\
                Year of completion: \\ 
                Institution \\ 
                Department \\
                \lipsum[1][1-4] \\

                \noindent
                \textbf{Degree Name} \\
                Year of completion: \\ 
                Institution \\ 
                Department \\
                \lipsum[1][1-4] \\
                
                \noindent
                \textbf{Position Title} \\
                Time Period: \\
                Institution \\ 
                Department \\
                \lipsum[1][1-4] \\
                
                \noindent
                \textbf{Position Title} \\
                Time Period: \\
                Institution \\ 
                Department \\
                \lipsum[1][1-4] 

            %------------------------
            % Publications Section
            \section*{PUBLICATIONS}
                \subsection*{Reviewed Articles}
                    \lipsum[1][5-11]
                \subsection*{Non-Reviewed Articles}
                    \lipsum[1][5-11]
                \subsection*{Books}
                    \lipsum[1][5-11]
                \subsection*{Book Chapters}
                    \lipsum[1][5-11]
                \subsection*{Abstracts}
                    \lipsum[1][5-11]
                \subsection*{Other}
                    \lipsum[1][5-11]

            %------------------------
            % Creative activity section
            \section*{CREATIVE ACTIVITY}
                \subsection*{Publications}
                    \lipsum[1][1-5]
                \subsection*{Presentations}
                    \lipsum[1][1-5]
                \subsection*{Performance}
                    \lipsum[1][1-5]
                \subsection*{Exhibition}
                    \lipsum[1][1-5]
                \subsection*{Projects}
                    \lipsum[1][1-5]

            %------------------------
            % Grants Section
            \section*{GRANTS}
                \subsection*{External Grants}
                \begin{subs}
                    \subsubsection*{Funded}
                        Proposal Title: \\
                        Funding Agency: \\
                        Role Status: \\
                        Percentage of Attributed Effort: \\
                        Total direct costs and annual budget:\\
                        Coverage Period:
                    \subsubsection*{Pending}
                        Proposal Title:\\
                        Funding Agency:\\
                        Role Status: \\
                        Percentage of Attributed Effort: \\
                        Total direct costs and annual budget:
                    \subsubsection*{Not Funded (Optional but recommended)}
                        Proposal Title:\\
                        Funding Agency:\\
                        Role Status: \\
                        Percentage of Attributed Effort: 
                \end{subs}
                \subsection*{Internal Grants}
                \begin{subs}
                    \subsubsection*{Funded}
                        Proposal Title:\\
                        Funding Agency:\\
                        Role Status: \\
                        Percentage of Attributed Effort: \\
                        Total direct costs and annual budget:\\
                        Coverage Period:
                    \subsubsection*{Pending}
                        Proposal Title:\\
                        Funding Agency:\\
                        Role Status: \\
                        Percentage of Attributed Effort: \\
                        Total direct costs and annual budget:
                    \subsubsection*{Not Funded (Optional but recommended)}
                        Proposal Title:\\
                        Funding Agency:\\
                        Role Status: \\
                        Percentage of Attributed Effort: 
                \end{subs}

            %------------------------
            % Teaching and Advising Section
            \section*{TEACHING AND ADVISING}
                \subsection*{Courses}
                    Course Title:\\
                    Term and Year Taught:\\
                    Number of Students:\\
                    Additional Course Information:
                \subsection*{Supervision of Graduate Students}
                    Student Name:\\
                    Candidate Level (masters, doctoral):\\
                    Completion Dates:\\
                    Thesis/Dissertation Title: 
                \subsection*{Supervision of Undergraduate Students}
                    Student Name:\\
                    Completion Dates:\\
                    Honors Thesis Title: 
                \subsection*{Advising Activities}
                    \lipsum[1][5-11]

            %------------------------
            % Service and Professional Development Section
            \section*{SERVICE \& PROFESSIONAL DEVELOPMENT}
                \subsection*{Service to the Institution}
                \begin{subs}
                    \subsubsection*{Department Service} 
                        \lipsum[1][5-8]
                    \subsubsection*{College Service}
                        \lipsum[1][5-8]
                    \subsubsection*{University Service}
                        \lipsum[1][5-8]
                \end{subs}
                \subsection*{Service to the Discipline and Profession}
                    \lipsum[1][3-9]
                \subsection*{Service to the Community and Public}
                    \lipsum[1][3-9]
                \subsection*{Professional Development}
                \lipsum[1][3-9]

            % End document
            \end{document}
            %-------------------------------------------------------------------------------
            %-------------------------------------------------------------------------------
        """
    },
    {
        'id': '2',
        'name': 'template 2',
        'thumbnail': r'server/assets/resume_thumbnail_id_2.jpeg',
        'latex':
        r"""
            \documentclass{resume} % Use the custom resume.cls style
            
            \usepackage[left=0.4 in,top=0.4in,right=0.4 in,bottom=0.4in]{geometry} % Document margins
            \newcommand{\tab}[1]{\hspace{.2667\textwidth}\rlap{#1}} 
            \newcommand{\itab}[1]{\hspace{0em}\rlap{#1}}
            \name{Firstname Lastname} % Your name
            % if you do not have a website, sub your github instead.
            \address{+1(123) 456-7890 \\ San Francisco, CA} 
            \address{\href{mailto:youremailhere@gmail.com}{youremailhere@gmail.com} \\ \href{https://linkedin.com/in/linkedinURL}{linkedin.com/in/linkedinURL} \\ \href{www.yourwebsite.com}{www.yourwebsite.com}}  %
            
            \begin{document}
            
            
            \begin{rSection}{PROJECTS}
            \vspace{-1.25em}
            \item \textbf{Project 1} {Language 1, Framework 1, Database, Language 2, Framework 2, DevOps Tooling, etc}
            \begin{itemize}
                \itemsep -3pt {} 
                 \item Created a XYZ feature to accomplish ABC.
                 \item Retrieved data from XYZ to for ABC.
                \item Implemented XYZ library for ABC.
                \item Utilized XYZ that increased A by B\%.
             \end{itemize}
            \item \textbf{Project 2} {Language 1, Framework 1, Database, Language 2, Framework 2, DevOps Tooling, etc}
            \begin{itemize}
                \itemsep -3pt {} 
                 \item Created a XYZ feature to accomplish ABC.
                 \item Retrieved data from XYZ to for ABC.
                \item Implemented XYZ library for ABC.
                \item Utilized XYZ that increased A by B\%.
             \end{itemize}
            \item \textbf{Project 3} {Language 1, Framework 1, Database, Language 2, Framework 2, DevOps Tooling, etc}
            \begin{itemize}
                \itemsep -3pt {} 
                 \item Created a XYZ feature to accomplish ABC.
                 \item Retrieved data from XYZ to for ABC.
                \item Implemented XYZ library for ABC.
                \item Utilized XYZ that increased A by B\%.
             \end{itemize}
            \item \textbf{Project 4} {Language 1, Framework 1, Database, Language 2, Framework 2, DevOps Tooling, etc} 
            \begin{itemize}
                \itemsep -3pt {} 
                 \item Created a XYZ feature to accomplish ABC.
                 \item Retrieved data from XYZ to for ABC.
                \item Implemented XYZ library for ABC.
                \item Utilized XYZ that increased A by B\%.
             \end{itemize}
            \end{rSection} 
            
            
            %----------------------------------------------------------------------------------------
            % make sure to list your skills from most comfortable to least comfortable
            % never put anything on here that you cant talk about in an interview
            \begin{rSection}{SKILLS}
            \begin{tabular}{ @{} >{\bfseries}l @{\hspace{6ex}} l }
            Languages & Javascript, Python, HTML, CSS, PostgreSQL, GraphQL \\
            Frameworks & React, Redux, Node.js, Express, Django, Mocha \\
            Tools & Git, Docker, TravisCI, Kubernetes, AWS\\
            \\
            Soft Skills & Time Management, Teamwork, Communication, Problem Solving, Leadership, Accountability
            \\
            \end{tabular}\\
            \end{rSection}
            
            
            %----------------------------------------------------------------------------------------
            \begin{rSection}{Education}
            
            
            {\bf Software Development Certificate}, XY Bootcamp \hfill {Month Year} \\
            {\bf BS in XYZ}, ABC University \hfill {Month Year}
            
            
            \end{rSection}
            
            %----------------------------------------------------------------------------------------
            %	WORK EXPERIENCE SECTION
            
            % include this if you want or have extra room
            %----------------------------------------------------------------------------------------
            
            \begin{rSection}{Work Experience}
            \vspace{-1.25em}
            \item \textbf{Job Title} {Company} \hfill Month Year - Month Year
            \item \textbf{Job Title} {Company} \hfill Month Year - Month Year
            \item \textbf{Job Title} {Company} \hfill Month Year - Month Year
            \end{rSection} 
            
            
            % \begin{rSection}{Awards}
            % \vspace{-1.25em}
            % \item \textbf{Title} {Brief description of what award was for} \hfill Jul 2019
            % \item \textbf{Title} {Brief description of what award was for} \hfill Jul 2019
            % \item \textbf{Title} {Brief description of what award was for} \hfill Jul 2019
            % \end{rSection} 
            
            
            \end{document}
        """
    },
    {
        'id': '3',
        'name': 'template 3',
        'thumbnail': r'server/assets/resume_thumbnail_id_3.jpeg',
        'latex':
        r"""
            % !TeX spellcheck = en_GB
            % !TeX program = pdflatex
            %
            % LuxSleek-CV 1.1 LaTeX template
            % Author: Andreï V. Kostyrka, University of Luxembourg
            %
            % 1.1: added tracking and letter-spacing for prettier lower caps, added `~` for language levels
            % 1.0: initial release
            %
            % This template fills the gap in the available variety of templates
            % by proposing something that is not a custom class, not using any
            % hard-coded settings deeply hidden in style files, and provides
            % a handful of custom command definitions that are as transparent as it gets.
            % Developed at the University of Luxembourg.
            %
            % *NOTHING IS HARCODED, and never should be.*
            %
            % Target audience: applicants in the IT industry, or business in general
            %
            % The main strength of this template is, it explicitly showcases how
            % to break the flow of text to achieve the most flexible right alignment
            % of dates for multiple configurations.

            \documentclass[11pt, a4paper]{article} 

            \usepackage[T1]{fontenc}     % We are using pdfLaTeX,
            \usepackage[utf8]{inputenc}  % hence this preparation
            \usepackage[british]{babel}  
            \usepackage[left = 0mm, right = 0mm, top = 0mm, bottom = 0mm]{geometry}
            \usepackage[stretch = 25, shrink = 25, tracking=true, letterspace=30]{microtype}  
            \usepackage{graphicx}        % To insert pictures
            \usepackage{xcolor}          % To add colour to the document
            \usepackage{marvosym}        % Provides icons for the contact details

            \usepackage{enumitem}        % To redefine spacing in lists
            \setlist{parsep = 0pt, topsep = 0pt, partopsep = 1pt, itemsep = 1pt, leftmargin = 6mm}

            \usepackage{FiraSans}        % Change this to use any font, but keep it simple
            \renewcommand{\familydefault}{\sfdefault}

            \definecolor{cvblue}{HTML}{304263}

            %%%%%%% USER COMMAND DEFINITIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%
            % These are the real workhorses of this template
            \newcommand{\dates}[1]{\hfill\mbox{\textbf{#1}}} % Bold stuff that doesn’t got broken into lines
            \newcommand{\is}{\par\vskip.5ex plus .4ex} % Item spacing
            \newcommand{\smaller}[1]{{\small$\diamond$\ #1}}
            \newcommand{\headleft}[1]{\vspace*{3ex}\textsc{\textbf{#1}}\par%
                \vspace*{-1.5ex}\hrulefill\par\vspace*{0.7ex}}
            \newcommand{\headright}[1]{\vspace*{2.5ex}\textsc{\Large\color{cvblue}#1}\par%
                \vspace*{-2ex}{\color{cvblue}\hrulefill}\par}
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

            \usepackage[colorlinks = true, urlcolor = white, linkcolor = white]{hyperref}

            \begin{document}

            % Style definitions -- killing the unnecessary space and adding the skips explicitly
            \setlength{\topskip}{0pt}
            \setlength{\parindent}{0pt}
            \setlength{\parskip}{0pt}
            \setlength{\fboxsep}{0pt}
            \pagestyle{empty}
            \raggedbottom

            \begin{minipage}[t]{0.33\textwidth} %% Left column -- outer definition
            %  Left column -- top dark rectangle
            \colorbox{cvblue}{\begin{minipage}[t][5mm][t]{\textwidth}\null\hfill\null\end{minipage}}

            \vspace{-.2ex} % Eliminates the small gap
            \colorbox{cvblue!90}{\color{white}  %% LEFT BOX
            \kern0.09\textwidth\relax% Left margin provided explicitly
            \begin{minipage}[t][293mm][t]{0.82\textwidth}
            \raggedright
            \vspace*{2.5ex}

            \Large Guillaume \textbf{\textsc{Ouancaux}} \normalsize 

            % Centering without extra vertical spacing
            \null\hfill\includegraphics[width=0.65\textwidth]{oval-transparent.png}\hfill\null

            \vspace*{0.5ex} % Extra space after the picture

            \headleft{Profile}
            Innovative and passionate \textbf{data analyst} with over 15~years of experience in the chocolate and confectionery industry, seeking to leverage extensive background in data analysis, flavour profiling, and market trends.
            Proficient in Python programming, I have successfully developed and maintained multiple scalable and efficient software applications.
            Demonstrated strong problem-solving skills by implementing optimised algorithms and data structures in Python, significantly improving system performance.

            \headleft{Contact details}
            \small % To fit more content
            \MVAt\ {\small wonky.william123@gmail.com} \\[0.4ex]
            \Mobilefone\ +352\,123\,456\,789 \\[0.5ex]
            \Mundus\ \href{https://github.com/WillyWonka}{github.com/WillyWonka} \\[0.1ex]
            \Letter\ 49 Paddocks Spring, Farthingtonshire SG2 9UD, UK
            \normalsize

            \headleft{Personal information}
            %Year of birth: \textbf{1861} \\[0.5ex]
            Citizenship: \textbf{United Kingdom} \\[0.5ex]
            Family: \textbf{Single without children} \\[0.5ex]
            Languages: \textbf{French}~(B2), \textbf{Luxembourgish}~(A2), \textbf{German}~(A1), \textbf{English}~(native)

            \headleft{Skills}
            \begin{itemize}
            \item Python, SQL, PySpark
            \item R, Matlab, Azure Databricks
            \item MS Word, Excel, PowerPoint
            \item Communication and team collaboration
            \end{itemize} 

            \end{minipage}%
            \kern0.09\textwidth\relax%%Right margin provided explicitly to stretch the colourbox
            }
            \end{minipage}% Right column
            \hskip2.5em% Left margin for the white area
            \begin{minipage}[t]{0.56\textwidth}
            \setlength{\parskip}{0.8ex}% Adds spaces between paragraphs; use \\ to add new lines without this space. Shrink this amount to fit more data vertically

            \vspace{2ex}

            \headright{Experience}

            \textsc{Senior data scientist} at \textit{Shockelasrull (Luxembourg).}  \dates{2021.04--pres.} \\
            \smaller{Natural language processing, topic modelling, olfactory analysis,  building chained processes, automation of reports.}

            \is % Item spacing -- defined in the preamble
            \textsc{Data scientist} at \textit{Chocky-Facky SA (United Kingdom).}  \dates{2019.02--2020.11} \\
            \smaller{Predictive models for consumer taste preferences, market trend analysis, advanced data visualisation, negotiations with stakeholders.}

            \is
            \textsc{Data analyst} at \textit{Chocolate River Factory (France).}  \dates{2018.02--2018.12} \\
            \smaller{Data collection processes, extensive research on carbonation levels, collaboration with product development teams.}

            \is
            \textsc{Research support} at \textit{Everlasting Gobstopper Ltd.\ (Mongolia).} \\ 
            % \null is necessary here because this is a manually enforced break
            % and \dates start with an \hfill that needs a \nukk
            \null\dates{2016.05--2018.01} \\[-\baselineskip]
            \smaller{Developing and implementing methods for inferring \\
            causal networks from time-series, analysis of customer feedback data, mathematical optimisation,  machine learning.}

            \is
            \textsc{Research intern} at \textit{Snozzberry Farms (Italy).} \dates{2015.04--2015.07} \\
            \smaller{Dashboard creation with BI tools, analysis of competitor strategies.}

            \is
            \textsc{Researcher} at \textit{Whipple-Scrumptious Fudgemallow Delight Inc.\ (Guadeloupe).} \dates{2013.09--2015.01} \\
            \smaller{Econometric modelling, market data analysis, translation.} 

            \is
            \textsc{Intern in logistics management} at \textit{Candy Confections (Egypt).} \\  
            \smaller{Data management with Microsoft Excel.} \dates{2012.04--2012.12}

            \is
            \textsc{Editor} at \textit{BEANS Publishing LLC (Japan).} \dates{2009.03--2011.10} \\
            \smaller{Editorial work on dentistry literature, proofreading.} 


            \headright{Education}

            \textsc{Master in Economics.} Mathematical Methods of Economic Analysis. \textit{University of Sweets and Treats}. \dates{2013--2015} \\
            \smaller{Thesis title: \textit{The Effect of Beverage Sugar Content on Their Shelf Life.}} \\
            \smaller{Econometric analysis, survival analysis, panel and time-series models.}

            \is
            \textsc{Bachelor of Science in Biology.} Faculty of Experimental Confectionery. \textit{Bolzmann State Technical University}.  \dates{2006--2010} \\
            \smaller{Mathematical modelling, numerical methods, mathematical optimisation.}


            \headright{Additional education}

            \textsc{Stanford introduction to food and health.}
            \textit{Coursera.} \dates{2021} \\
            \smaller{Contemporary trends in eating, cooking workshop, future directions in health.}

            \is
            \textsc{Topical courses -- Master in Chocolate Sculpting.}
            \textit{University of Cocoa.} \dates{2015--2017} \\
            \smaller{Data science, statistics and probability,  food science, agricultural science, optimal stopping theory, cultural studies in food.}


            \headright{Hobbies}

            \textit{Music:} imitating birds on the banjo, composing and decomposing (morally).

            \textit{Poetry:} inventing rhymes, surreal art.

            \textit{Miscellaneous:} zoology, mycology, trainspotting, 1930s horror films.
            \end{minipage}

            \end{document}
        """
    }

]