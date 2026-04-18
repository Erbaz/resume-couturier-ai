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
            \documentclass[11pt,a4paper]{article} % Use standard article class
            
            \usepackage[T1]{fontenc}
            \usepackage[utf8]{inputenc}
            \usepackage[left=0.4 in,top=0.4in,right=0.4 in,bottom=0.4in]{geometry} % Document margins
            \usepackage{parskip} % For paragraph spacing
            \usepackage{array} % For table formatting
            \usepackage{ifthen} % For conditional logic
            \usepackage{hyperref} % For links

            \makeatletter
            % --- Inline Official Resume Class Definitions ---
            \def \name#1{\def\@name{#1}} % Defines the \name command to set name
            \def \@name {} % Sets \@name to empty by default

            \def \addressSep {$\diamond$} % Set default address separator to a diamond

            % One, two or three address lines can be specified 
            \let \@addressone \relax
            \let \@addresstwo \relax
            \let \@addressthree \relax

            % \address command can be used to set the first, second, and third address (last 2 optional)
            \def \address #1{
              \@ifundefined{@addresstwo}{
                \def \@addresstwo {#1}
              }{
              \@ifundefined{@addressthree}{
              \def \@addressthree {#1}
              }{
                 \def \@addressone {#1}
              }}
            }

            % \printaddress is used to style an address line (given as input)
            \def \printaddress #1{
              \begingroup
                \def \\ {\addressSep\ }
                \centerline{#1}
              \endgroup
              \par
              \addressskip
            }

            % \printname is used to print the name as a page header
            \def \printname {
              \begingroup
                \hfil{\MakeUppercase{\namesize\bf \@name}}\hfil
                \nameskip\break
              \endgroup
            }

            %----------------------------------------------------------------------------------------
            %	PRINT THE HEADING LINES
            %----------------------------------------------------------------------------------------

            \let\ori@document=\document
            \renewcommand{\document}{
              \ori@document  % Begin document
              \printname % Print the name specified with \name
              \@ifundefined{@addressone}{}{ % Print the first address if specified
                \printaddress{\@addressone}}
              \@ifundefined{@addresstwo}{}{ % Print the second address if specified
                \printaddress{\@addresstwo}}
                 \@ifundefined{@addressthree}{}{ % Print the third address if specified
                \printaddress{\@addressthree}}
            }

            %----------------------------------------------------------------------------------------
            %	SECTION FORMATTING
            %----------------------------------------------------------------------------------------

            % Defines the rSection environment for the large sections within the CV
            \newenvironment{rSection}[1]{ % 1 input argument - section name
              \sectionskip
              \MakeUppercase{\bf #1} % Section title
              \sectionlineskip
              \hrule % Horizontal line
              \begin{list}{}{ % List for each individual item in the section
                \setlength{\leftmargin}{1.5em} % Margin within the section
              }
              \item[]
            }{
              \end{list}
            }

            %----------------------------------------------------------------------------------------
            %	WORK EXPERIENCE FORMATTING
            %----------------------------------------------------------------------------------------

            \newenvironment{rSubsection}[4]{ % 4 input arguments - company name, year(s) employed, job title and location
             {\bf #1} \hfill {#2} % Bold company name and date on the right
             \ifthenelse{\equal{#3}{}}{}{ % If the third argument is not specified, don't print the job title and location line
              \\
              {\em #3} \hfill {\em #4} % Italic job title and location
              }\smallskip
              \begin{list}{$\cdot$}{\leftmargin=0em} % \cdot used for bullets, no indentation
               \itemsep -0.5em \vspace{-0.5em} % Compress items in list together for aesthetics
              }{
              \end{list}
              \vspace{0.5em} % Some space after the list of bullet points
            }

            % The below commands define the whitespace after certain things in the document - they can be \smallskip, \medskip or \bigskip
            \def\namesize{\huge} % Size of the name at the top of the document
            \def\addressskip{\smallskip} % The space between the two address (or phone/email) lines
            \def\sectionlineskip{\medskip} % The space above the horizontal line for each section 
            \def\nameskip{\bigskip} % The space after your name at the top
            \def\sectionskip{\medskip} % The space after the heading section
            \makeatother
            % --- End of Inline Definitions ---

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
        r"""%-----------------------------------------------------------------------------------------------------------------------------------------------%
            %	The MIT License (MIT)
            %
            %	Copyright (c) 2021 Jitin Nair
            %
            %	Permission is hereby granted, free of charge, to any person obtaining a copy
            %	of this software and associated documentation files (the "Software"), to deal
            %	in the Software without restriction, including without limitation the rights
            %	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
            %	copies of the Software, and to permit persons to whom the Software is
            %	furnished to do so, subject to the following conditions:
            %	
            %	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
            %	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
            %	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
            %	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
            %	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
            %	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
            %	THE SOFTWARE.
            %	
            %
            %-----------------------------------------------------------------------------------------------------------------------------------------------%

            %----------------------------------------------------------------------------------------
            %	DOCUMENT DEFINITION
            %----------------------------------------------------------------------------------------

            % article class because we want to fully customize the page and not use a cv template
            \documentclass[a4paper,12pt]{article}

            %----------------------------------------------------------------------------------------
            %	FONT
            %----------------------------------------------------------------------------------------

            % % fontspec allows you to use TTF/OTF fonts directly
            % \usepackage{fontspec}
            % \defaultfontfeatures{Ligatures=TeX}

            % % modified for ShareLaTeX use
            % \setmainfont[
            % SmallCapsFont = Fontin-SmallCaps.otf,
            % BoldFont = Fontin-Bold.otf,
            % ItalicFont = Fontin-Italic.otf
            % ]
            % {Fontin.otf}

            %----------------------------------------------------------------------------------------
            %	PACKAGES
            %----------------------------------------------------------------------------------------
            \usepackage{url}
            \usepackage{parskip} 	

            %other packages for formatting
            \RequirePackage{color}
            \RequirePackage{graphicx}
            \usepackage[usenames,dvipsnames]{xcolor}
            \usepackage[scale=0.9]{geometry}

            %tabularx environment
            \usepackage{tabularx}

            %for lists within experience section
            \usepackage{enumitem}

            % centered version of 'X' col. type
            \newcolumntype{C}{>{\centering\arraybackslash}X} 

            %to prevent spillover of tabular into next pages
            \usepackage{supertabular}
            \usepackage{tabularx}
            \newlength{\fullcollw}
            \setlength{\fullcollw}{0.47\textwidth}

            %custom \section
            \usepackage{titlesec}				
            \usepackage{multicol}
            \usepackage{multirow}

            %CV Sections inspired by: 
            %http://stefano.italians.nl/archives/26
            \titleformat{\section}{\Large\scshape\raggedright}{}{0em}{}[\titlerule]
            \titlespacing{\section}{0pt}{10pt}{10pt}

            %for publications
            \usepackage[style=authoryear,sorting=ynt, maxbibnames=2]{biblatex}

            %Setup hyperref package, and colours for links
            \usepackage[unicode, draft=false]{hyperref}
            \definecolor{linkcolour}{rgb}{0,0.2,0.6}
            \hypersetup{colorlinks,breaklinks,urlcolor=linkcolour,linkcolor=linkcolour}
            \addbibresource{citations.bib}
            \setlength\bibitemsep{1em}

            %for social icons
            \usepackage{fontawesome5}

            %debug page outer frames
            %\usepackage{showframe}


            % job listing environments
            \newenvironment{jobshort}[2]
                {
                \begin{tabularx}{\linewidth}{@{}l X r@{}}
                \textbf{#1} & \hfill &  #2 \\[3.75pt]
                \end{tabularx}
                }
                {
                }

            \newenvironment{joblong}[2]
                {
                \begin{tabularx}{\linewidth}{@{}l X r@{}}
                \textbf{#1} & \hfill &  #2 \\[3.75pt]
                \end{tabularx}
                \begin{minipage}[t]{\linewidth}
                \begin{itemize}[nosep,after=\strut, leftmargin=1em, itemsep=3pt,label=--]
                }
                {
                \end{itemize}
                \end{minipage}    
                }



            %----------------------------------------------------------------------------------------
            %	BEGIN DOCUMENT
            %----------------------------------------------------------------------------------------
            \begin{document}

            % non-numbered pages
            \pagestyle{empty} 

            %----------------------------------------------------------------------------------------
            %	TITLE
            %----------------------------------------------------------------------------------------

            % \begin{tabularx}{\linewidth}{ @{}X X@{} }
            % \huge{Your Name}\vspace{2pt} & \hfill \emoji{incoming-envelope} email@email.com \\
            % \raisebox{-0.05\height}\faGithub\ username \ | \
            % \raisebox{-0.00\height}\faLinkedin\ username \ | \ \raisebox{-0.05\height}\faGlobe \ mysite.com  & \hfill \emoji{calling} number
            % \end{tabularx}

            \begin{tabularx}{\linewidth}{@{} C @{}}
            \Huge{Your Name} \\[7.5pt]
            \href{https://github.com/username}{\raisebox{-0.05\height}\faGithub\ username} \ $|$ \ 
            \href{https://linkedin.com/in/username}{\raisebox{-0.05\height}\faLinkedin\ username} \ $|$ \ 
            \href{https://mysite.com}{\raisebox{-0.05\height}\faGlobe \ mysite.com} \ $|$ \ 
            \href{mailto:email@mysite.com}{\raisebox{-0.05\height}\faEnvelope \ email@mysite.com} \ $|$ \ 
            \href{tel:+000000000000}{\raisebox{-0.05\height}\faMobile \ +00.00.000.000} \\
            \end{tabularx}

            %----------------------------------------------------------------------------------------
            % EXPERIENCE SECTIONS
            %----------------------------------------------------------------------------------------

            %Interests/ Keywords/ Summary
            \section{Summary}
            This CV can also be automatically complied and published using GitHub Actions. For details, \href{https://github.com/jitinnair1/autoCV}{click here}.

            %Experience
            \section{Work Experience}

            \begin{jobshort}{Designation}{Jan 2021 - present}
            long long line of blah blah that will wrap when the table fills the column width long long line of blah blah that will wrap when the table fills the column width long long line of blah blah that will wrap when the table fills the column width long long line of blah blah that will wrap when the table fills the column width
            \end{jobshort}


            \begin{joblong}{Designation}{Mar 2019 - Jan 2021}
            \item long long line of blah blah that will wrap when the table fills the column width
            \item again, long long line of blah blah that will wrap when the table fills the column width but this time even more long long line of blah blah. again, long long line of blah blah that will wrap when the table fills the column width but this time even more long long line of blah blah
            \end{joblong}
            
            %Projects
            \section{Projects}

            \begin{tabularx}{\linewidth}{ @{}l r@{} }
            \textbf{Some Project} & \hfill \href{https://some-link.com}{Link to Demo} \\[3.75pt]
            \multicolumn{2}{@{}X@{}}{long long line of blah blah that will wrap when the table fills the column width long long line of blah blah that will wrap when the table fills the column width long long line of blah blah that will wrap when the table fills the column width long long line of blah blah that will wrap when the table fills the column width}  \\
            \end{tabularx}

            %----------------------------------------------------------------------------------------
            %	EDUCATION
            %----------------------------------------------------------------------------------------
            \section{Education}
            \begin{tabularx}{\linewidth}{@{}l X@{}}	
            2030 - present & PhD (Subject) at \textbf{University} \hfill \normalsize (GPA: 4.0/4.0) \\

            2023 - 2027 & Bachelor's Degree at \textbf{College} \hfill (GPA: 4.0/4.0) \\ 

            2022 & Class 12th Some Board \hfill  (Grades) \\

            2021 & Class 10th Some Board \hfill  (Grades) \\
            \end{tabularx}

            %----------------------------------------------------------------------------------------
            %	PUBLICATIONS
            %----------------------------------------------------------------------------------------
            \section{Publications}
            \begin{refsection}[citations.bib]
            \nocite{*}
            \printbibliography[heading=none]
            \end{refsection}

            %----------------------------------------------------------------------------------------
            %	SKILLS
            %----------------------------------------------------------------------------------------
            \section{Skills}
            \begin{tabularx}{\linewidth}{@{}l X@{}}
            Some Skills &  \normalsize{This, That, Some of this and that etc.}\\
            Some More Skills  &  \normalsize{Also some more of this, Some more that, And some of this and that etc.}\\  
            \end{tabularx}

            \vfill
            \center{\footnotesize Last updated: \today}

            \end{document}
        """
    }

]