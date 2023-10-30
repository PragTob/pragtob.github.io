wkhtmltopdf --footer-left "Tobias Pfeiffer" --footer-right "[page]/[toPage]" --enable-local-file-access _site/resume_print.html tobias_pfeiffer_resume.pdf 
wkhtmltopdf --footer-right "[page]/[toPage]" --enable-local-file-access _site/anonymous_resume_print.html anonymous_resume.pdf

