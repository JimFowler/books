;; Begin copyright
;;
;;  /home/jrf/Documents/books/Books20/Tools/emacs/books20.el
;;  
;;   Part of the Books20 Project
;;
;;   Copyright 2018 James R. Fowler
;;
;;   All rights reserved. No part of this publication may be
;;   reproduced, stored in a retrival system, or transmitted
;;   in any form or by any means, electronic, mechanical,
;;   photocopying, recording, or otherwise, without prior written
;;   permission of the author.
;;
;;
;; End copyright


;;  
;;   Emacs commands that I use for my Books20 project.
;;
;; Will this work in AquaEmacs on a Mac as well
;; as emacs25 or XEmacs on a Linux system?
;;
;; Need to fix comment characters in this function
;;
;; Useful variable and command
;; (defvar fext (file-name-extension (file)))
;; we care about py, tex, txt, bib, NIL (defaults to text),
;;  el (emacs files), c, h, cpp, sh, csh, m (octave), 
;;
;; (user-full-name) == Jim Fowler
;;

(provide 'books20)

(defun replace-comments (ext)
  "replace the original LaTex comment characters '%%' with the
   appropriate comment characters for this file type as found
   with the file extension. If no file extension is found, do
   nothing. Need to add XML and XSD files to this list."
  (interactive)
  (defvar ext-replace "")
  (cond ((string= ext "py")  (setq ext-replace "##"))
	((string= ext "rst") (setq ext-replace ".. "))
	((string= ext "csh") (setq ext-replace "##"))
	((string= ext "sh")  (setq ext-replace "##"))
	((string= ext "el")  (setq ext-replace ";;"))
	((string= ext "tex") (setq ext-replace "%%"))
	((string= ext "bib") (setq ext-replace "%%"))
	((string= ext "am")  (setq ext-replace "#"))
	((string= ext "ac")  (setq ext-replace "dnl"))
	((string= ext "txt") (setq ext-replace ""))
	((string= ext "xml") (setq ext-replace ""))
	((string= ext "xsd") (setq ext-replace ""))
	((string= ext "php") (setq ext-replace ""))
	((string= ext "html") (setq ext-replace ""))
	(t (setq ext-replace "%%"))
	)
  (while (search-forward "%%" nil t) (replace-match ext-replace))
  )

(defun insert-copyright ()
  "Insert current author and copyright statement."
  (interactive)
  (defvar file-ext "")
  (setq file-ext (file-name-extension buffer-file-name))
  (save-restriction 
    (narrow-to-region (point) (point))
    (insert-file-contents (expand-file-name "~/Emacs/Files/generic_copyright.tex"))
    (goto-char (point-min))
    (replace-comments file-ext)
    (message "%s has point-min %d and point-max %d" buffer-file-name (point-min) (point-max))
    (goto-char (point-min))
    (while (search-forward "[User]" nil t) (replace-match user-login-name))
    (goto-char (point-min))
    (while (search-forward "[File]" nil t) (replace-match buffer-file-name))
    (goto-char (point-min))
    (while (search-forward "[Year]" nil t) (replace-match  (substring (current-time-string) 20 24)))
    (goto-char (point-min))
    (while (search-forward "[Date]" nil t) (replace-match (substring (current-time-string) 0 10)))
    (goto-char (point-min))
    (if (or (string= file-ext "xml") (string= file-ext "xsd")
	    (string= file-ext "html") (string= file-ext "php"))
	(progn
	  (goto-char (point-min))
	  (while (search-forward "Begin copyright" nil t 1) (replace-match "<!-- Begin copyright"))
	  (goto-char (point-min))
	  (while (search-forward "End copyright" nil t 1) (replace-match "End copyright -->"))
	  )
      )
    (goto-char (point-max))
    )
  )

(defun replace-copyright ()
  "Replace the existing copyright notice with a new one"
  (interactive)
  )
