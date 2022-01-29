This project has been taught by Patrick Collins from Solidity, Blockchain, and Smart Contract Course - Beginner to Expert Python Tutorial.

1. This Smart Contract allow users to enter into a pool of lottery during the LOTTERY_STATE.OPEN
2. After the admin has issued the end_lottery() in the deploy_lotter.py, the state changes to LOTTERY_STATE.CALCULATING_WINNER. New users can't enter the lottery anymore.
3. The end_lottery() calls the endLottery() function in Lottery.sol which then calls the RequestRandom function. 
4. RequestRandom function interally calls the fufillRandomness function, which will generate a random number using Chainlink VRF.
5. The random number will choose the users that are stored in the players[] array and will automatically pay out the prize pool to the wallet address that the user has previously entered the lottery with.
6. The function the closes the lottery by declaring LOTTERY_STATE.CLOSED, allowing the lottery to be reopened again to public. 
