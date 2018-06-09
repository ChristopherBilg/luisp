(define not
    (lambda (x) 
        (if x False True)))
(define append 
    (lambda (l1 l2) 
        (if (null? l1) l2 (cons (car l1) (append (cdr l1) l2)))))
(define pair 
    (lambda (x y)
        (cons x (cons y (q ())))))
(define caar 
    (lambda (x)
        (car (car x))))
(define cadr 
    (lambda (x)
        (car (cdr x))))
(define cddr
    (lambda (x)
        (cdr (cdr x))))
(define cdar
    (lambda (x)
        (cdr (car x))))
(define cadar
    (lambda (x)
        (cadr (car x))))
(define caddr
    (lambda (x)
        (cadr (cdr x))))
(define caddar
    (lambda (x)
        (caddr (car x))))
(define pairlis 
    (lambda (x y)
        (if (null? x)
            (q ()) 
            (cons (pair (car x) (car y)) (pairlis (cdr x) (cdr y))))))
(define assoc 
    (lambda (k1 l1) 
        (if (eq? (caar l1) k1) 
            (cadar l1) 
            (assoc k1 (cdr l1)))))

(define a (pairlis (quote (1 2 3)) (quote (4 5 6))))
(assoc 2 a)