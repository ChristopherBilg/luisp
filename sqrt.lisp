(define abs (lambda (x) (if (> x 0) x (- 0 x))))
(define average (lambda (a b) (/ (+ a b) 2)))

(define square (lambda(x) (* x x)))

(define sqrt (lambda (x) (sqrt-iter 1.0 x)))

(define sqrt-iter (lambda (guess x) (if (good-enough? guess x) guess (sqrt-iter (improve2 guess x) x))))

(define good-enough? (lambda (guess x) (< (abs (- (square guess) x)) 0.00001)))

(define improve (lambda (guess x) (- guess (/ (f guess x) (f-prime guess)))))

(define improve2 (lambda (guess x) (average guess (/ x guess))))

(define f (lambda (x x-squared) (- (square x) x-squared)))

(define f-prime (lambda (x) (* 2 x)))

(sqrt-iter 1.0 9)

(good-enough? 3 9)
(good-enough? 3 25)
(good-enough? 5 25)

(improve 3 9)

(f 3 9)

(f-prime 3)

(sqrt 9)
(sqrt 25)
(sqrt 2.0)

(average 1 2)
(improve2 3 9)
