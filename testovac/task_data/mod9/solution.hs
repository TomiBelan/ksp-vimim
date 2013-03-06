main :: IO()
main = do
	s <- getLine
	putStrLn (show (mod (sum [read [c]::Int | c<-s ]) 9 == 0))
