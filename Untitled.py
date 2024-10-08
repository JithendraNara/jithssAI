secret_code= input("Enter a 4 digit code with n0 repeating values: ")
while len(set(secret_code))!=4:
    secret_code = input("Enter a 4 digit code with no repeating values: ")
def jith():
    

    tries=0
    while True:
        guess = input("Enter your guess: ")
        
        while len(set(guess))!=4:
            guess = input("Enter a 4 digit code with no repeating values: ")
        bulls=0
        cows=0
    
        for i in range(4):
            if guess[i] == secret_code[i]:
                bulls = bulls+1
            elif (guess[i] != secret_code[i]) and (guess[i] in secret_code) :
                cows =cows+ 1
        tries = tries+1
        print(f"{bulls} bulls, {cows} cows")
        if bulls == 4:
            print(f"you guessed in {tries} tries")
            break
jith()