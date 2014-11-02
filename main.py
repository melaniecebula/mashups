import markov

def main():
	f = open('./m4.txt')
	f2 = open('./starwars.txt')
	m = markov.Markov(f, f2)
	print m.generate_markov_text(200)

if __name__ == "__main__":
    main()

 
