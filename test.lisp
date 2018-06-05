(pair2 1)
(pair2 2)

(define x (q ()))
(cons 1 x)
(cons 2 x)

(define set! (lambda (exp, val) (define exp val)))

(caar (q ((q (1)) 2)))
(car (car (q ((q (1)) 2))))
(car (q (1)))


(caar (q ((q (1)) 2)))
(cadr (q ((q (1 2)) 3)))
(cdar (q ((q (1 2)) 3 4)))
(cddr (q ((q (1 2)) 3 4)))

(caddar (q ((q (1 2 3 4)) 2)))


(cons 1 (cons 2 (q ())))
(pairlis (q (1 2 3)) (q (4 5 6)))
(define deepcar (lambda (x) (if (null? x) (q ()) (cdr (deepcar x)))))

(define fact (lambda (x) (if (eq? x 0) 1 (* x (fact (- x 1))))))
(fact 5)

(define factcons (lambda (x) (if (eq? x 0) (q ()) (cons (pair2 x x) (factcons (- x 1)))))))
(factcons 5)
(pairlis (q (1 2 3)) (q (4 5 6)))
(pairlis (q (1 2 3)) (q (4 5 6)))
(pairlis (q (1 2 3)) (q (4 5 6)))

(define constest (lambda (x y) (cons x (cons y (q ())))))
(constest 1 2)
(constest 1 2)
(constest 1 2)
