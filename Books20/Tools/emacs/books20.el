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


(defun replace-comments ()
  "replace the original LaTex comment characters '%%' with the
   appropriate comment characters for this file type as found
   with the file extension. If no file extension is found, do
   nothing."
  (setq a (file-name-extension buffer-file-name))
  (cond ((string= a "py") (replace-string "%%" "##"))
	((string= a "csh") (replace-string "%%" "##"))
	((string= a "sh") (replace-string "%%" "##"))
	((string= a "el") (replace-string "%%" ";;"))
	((string= a "tex") (replace-string "%%" "%%"))
	((string= a "bib") (replace-string "%%" "%%"))
	((string= a "am") (replace-string "%%" "#"))
	((string= a "ac") (replace-string "%%" "dnl"))
	((string= a "txt") (replace-string "%%" ""))
	)
  )

(defun insert-copyright ()
  "Insert current author and copyright statement."
  (interactive)
  (save-restriction 
    (narrow-to-region (point) (point))
    (insert-file-contents (expand-file-name "~/Emacs/Files/generic_copyright.tex"))
    (goto-char (point-min))
    (replace-comments)
    (goto-char (point-min))
    (replace-string "[User]" (user-login-name))
    (goto-char (point-min))
    (replace-string "[File]" buffer-file-name)
    (goto-char (point-min))
    (replace-string "[Year]" (substring (current-time-string) 20 24))
    (goto-char (point-min))
    (replace-string "[Date]" (substring (current-time-string) 0 10))
    (goto-char (point-max))
    )
  )

(defun replace-copyright ()
  "Replace the existing copyright notice with a new one"
  (interactive)
  )
