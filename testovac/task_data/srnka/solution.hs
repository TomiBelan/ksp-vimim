main :: IO()
main = do
	s <- getLine
	if s == "emacs" then putStrLn "ano" else putStrLn "nie"
