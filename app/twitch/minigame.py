import json
import random
import asyncio
import app.logging as log
import app.twitch.request as request
from decimal import Decimal, ROUND_HALF_UP
import os
from dotenv import load_dotenv

load_dotenv()



# duel class
class Duel():
    def __init__(self):
        self.filename = 'json/twitch/minigame.json'
        self.bet = None

        self.challenger = None
        self.challenger_balance = None

        self.challenged = None
        self.challenged_balance = None


    # saves the duel "request" to the minigame.json
    async def duel(self, bet: int, challenger: str, challenged: str):
        try:
            self.bet = bet
            self.challenger = challenger
            self.challenged = challenged

            try:
                with open(self.filename, 'r') as load_file:
                    minigame_json = json.load(load_file)
                    duel_dict = minigame_json['duel']
                    currency_dict = minigame_json['currency']
            except:
                minigame_json = {'duel': {}}
                duel_dict = minigame_json['duel']

            try:
                self.challenger_balance = currency_dict[f'{self.challenger}']
            except:
                self.challenger_balance = 0
            try:
                self.challenged_balance = currency_dict[f'{self.challenged}']
            except:
                self.challenged_balance = 0

            for keys in duel_dict:
                data = duel_dict[f'{keys}']
                if self.challenger == data['challenger'] or self.challenger == data['challenged']:
                    message = f'@{self.challenger} du hast schon jemanden herausgefordert oder wurdest schon herausgefordert'
                    return message, False
                elif self.challenged == data['challenger'] or self.challenged == data['challenged']:
                    message = f'@{self.challenger} dein Gegner hat schon jemanden herausgefordert oder wurde schon herausgefortet' 
                    return message, False
            else:
                if self.challenger == self.challenged:
                    message = f'@{self.challenger} du kannst dich nicht selber herausfordern louisd15Kek'
                    return message, False
                elif self.bet > self.challenged_balance or self.bet > self.challenger_balance:
                    message =  f'@{self.challenger} einer von euch hat zu wenig Stonks für den Kampf louisd15Cry'
                    return message, False

            self.next_key = str(max(map(int, duel_dict.keys()), default=0) + 1)

            duel_dict[f'{self.next_key}'] = {'bet': self.bet, 'challenger': self.challenger, 'challenged': self.challenged, 'accepted': 'None', 'exited': False}

            with open(self.filename, 'w') as save_file:
                json.dump(minigame_json, save_file, indent=4)

            if self.bet > 0:
                message = f'@{self.challenger} hat @{self.challenged} zu einen Duell um {self.bet} stonks herausgefortet! KomodoHype \n@{self.challenged} nimmst du das Duell an?'
            else:
                message = f'@{self.challenger} hat @{self.challenged} zu einen Duell herausgefortet! KomodoHype \n@{self.challenged} nimmst du das Duell an?'
            message = message + f' \nDu hast 60s zeit! !accept oder !deny'
            return message, True
        
        except Exception as err:
            error = f'[Twitch Minigame] (Duel) | Error in duel: {err}'
            log.log_error(error)


    # saves the accepted to true
    async def duel_accept(self, challanged):
        try:
            try:
                with open(self.filename, 'r') as load_file:
                    minigame_json = json.load(load_file)
                    duel_dict = minigame_json['duel']
            except:
                return
            
            for keys in duel_dict:
                data = duel_dict[keys]
                if challanged == data['challenged']:
                    data['accepted'] = True

                    with open(self.filename, 'w') as save_file:
                        json.dump(minigame_json, save_file, indent=4)
                    
                    return
            else:
                message = f'@{challanged} du wurdst von niemanden herausgefordert louisd15Wah'
                return message
            
        except Exception as err:
            error = f'[Twitch Minigame] (Duel) Error in duel_accept: {err}'
            log.log_error(error)
    

    # saves the accepted to false
    async def duel_deny(self, challanged):
        try:
            try:
                with open(self.filename, 'r') as load_file:
                    minigame_json = json.load(load_file)
                    duel_dict = minigame_json['duel']
            except:
                return
            
            for keys in duel_dict:
                data = duel_dict[keys]
                if challanged == data['challenged']:
                    data['accepted'] = False

                    with open(self.filename, 'w') as save_file:
                        json.dump(minigame_json, save_file, indent=4)

                    message = f'@{challanged} hat das Duell abgelehnt!'
                    return message
            else:
                message = f'@{challanged} du wurdest von niemanden herausgefordert louisd15Wah'
                return message

        except Exception as err:
            error = f'[Twitch Minigame] (Duel) Error in duel_deny: {err}'
            log.log_error(error)


    # saves the exited to true
    async def duel_exit(self, challenger):
        try:
            try:
                with open(self.filename, 'r') as load_file:
                    minigame_json = json.load(load_file)
                    duel_dict = minigame_json['duel']
            except:
                minigame_json = {'duel': {}}
                duel_dict = {}

            for keys in duel_dict:
                data = duel_dict[keys]
                if challenger == data['challenger']:
                    challenged = data['challenged']
                    data['exited'] = True
                    with open(self.filename, 'w') as save_file:
                        json.dump(minigame_json, save_file, indent=4)

                    message = f'@{challenger} hat das Duell gegen {challenged} abgebrochen NotLikeThis'
                    return message
            else:
                message = f'@{challenger} du niemanden zum Duell herausgefordert LUL'
                return message

        except Exception as err:
            error = f'[Twitch Minigame] (Duel) Error in duel_exit: {err}'
            log.log_error(error)


    # delete the duel from the duel dict
    async def duel_delete(self, challenger):
        try:
            try:
                with open(self.filename, 'r') as load_file:
                    minigame_json = json.load(load_file)
                    duel_dict = minigame_json.get('duel', {})
            except:
                minigame_json = {'duel': {}}
                duel_dict = {}

            for key in list(duel_dict.keys()):
                data = duel_dict[key]
                if challenger == data['challenger']:
                    duel_dict.pop(key)
                    with open(self.filename, 'w') as save_file:
                        json.dump(minigame_json, save_file, indent=4)
                    return
            
            return
            
        except Exception as err:
            error = f'[Twitch Minigame] (Duel) Error in duel_delete: {err}'
            log.log_error(error)
    

    # checks for 60s for an accept, if accepted is true returns true, if accepted is false return false 
    async def duel_wait_for_accept(self):
        index = 0
        while index != 60:
            await asyncio.sleep(1)
            index += 1

            try:
                with open(self.filename, 'r') as load_file:
                    minigame_json = json.load(load_file)
                    duel_dict = minigame_json['duel']
            except:
                minigame_json = {'duel': {}}
                duel_dict = {}

            for keys in duel_dict:
                data = duel_dict[f'{keys}']
                if self.challenger == data['challenger'] and self.challenged == data['challenged']:
                    if data['accepted'] == True:
                        return True
                    elif data['accepted'] == False or data['exited'] == True:
                        return False

        raise asyncio.exceptions.TimeoutError
    

    # if was_accepted is true, it choose randomly a winner and saves every thing to the minigame.json
    async def duel_is_valid(self):
        try:
            try:
                was_accepted = await asyncio.wait_for(self.duel_wait_for_accept(), 61)
                if not was_accepted:
                    await self.duel_delete(self.challenger)
                    return
            except asyncio.exceptions.TimeoutError:
                await self.duel_delete(self.challenger)
                message = f'@{self.challenged} hat das Duel nicht angenommen louisd15Wah'
                return message
            
            with open(self.filename, 'r') as load_file:
                minigame_json = json.load(load_file)
                currency_dict = minigame_json.get('currency', {})
                
            duellist_list = [self.challenger, self.challenged]
            winner = random.choice(duellist_list)

            if winner == self.challenger:
                message = f'@{self.challenger} du hast das Duell gegen @{self.challenged} gewonnen!'
                currency_dict[f'{self.challenged}'] = self.challenged_balance - self.bet
                currency_dict[f'{self.challenger}'] = self.challenger_balance + self.bet
            else:
                message = f'@{self.challenged} du hast das Duell gegen @{self.challenger} gewonnen!'
                currency_dict[f'{self.challenger}'] = self.challenger_balance - self.bet
                currency_dict[f'{self.challenged}'] = self.challenged_balance + self.bet

            with open(self.filename, 'w') as save_file:
                json.dump(minigame_json, save_file, indent=4)

            await self.duel_delete(self.challenger)

            return message

        except Exception as err:
            error = f'[Twitch Minigame] (Duel) Error in duel_is_valid: {err}'
            log.log_error(error)


    # deletes every duel from the duel dict
    async def duel_clear_dict(self):
        try:
            try:
                with open(self.filename, 'r') as load_file:
                    minigame_json = json.load(load_file)
                    duel_dict = minigame_json.get('duel', {})
            except:
                minigame_json = {'duel': {}}
                duel_dict = {}

            for key in list(duel_dict.keys()):
                duel_dict.pop(key)
            
            with open(self.filename, 'w') as save_file:
                json.dump(minigame_json, save_file, indent=4)

            return
        
        except Exception as err:
            error = f'[Twitch Minigame] (Duel) Error in duel_clear_dict: {err}'
            log.log_error(error)



# currency class
class Currency():
    def __init__(self):
        self.filename = 'json/twitch/minigame.json'
        self.watch_reward = 10
        self.is_live = False
        self.follower_list = None
        self.chatter_list = None
        self.currency_dict = None
        self.currency_counter = {}
        self.blocked_user_list = [str(os.getenv('TWITCH_CHATBOT_NAME'))]


    # on bot start it checks if there are new follower and initialize them to the balance dict
    async def initialize_currency(self):
        try:
            self.follower_list = request.get_channel_followers()
            self.chatter_list = request.get_channel_chatters()

            try:
                with open(self.filename, 'r') as load_file:
                    minigame_json = json.load(load_file)
                    self.currency_dict = minigame_json.get('currency', {})
            except:
                minigame_json['currency'] = {}
                self.currency_dict = minigame_json.get('currency', {})

            for follower in self.follower_list:
                if follower not in self.currency_dict:
                    self.currency_dict[f'{follower}'] = 0

            with open(self.filename, 'w') as save_file:
                json.dump(minigame_json, save_file, indent=4)

            #log.log_info(f'[MINIGAME] log currency_dict in initialize: {self.currency_dict}')
        
        except Exception as err:
            error = f'[Twitch Minigame] (Balance) Error in initialize_currency: {err}'
            log.log_error(error)
 

    # every 10 min it add 10 stonks to the balance for follower that watchting the stream live
    async def currency_loop(self):
        while True:
            try:
                if self.currency_counter and self.is_live:
                    for follower in self.currency_counter:
                        if follower in self.blocked_user_list:
                            pass

                        else:
                            watch_counter = self.currency_counter[f'{follower}']

                            if follower in self.chatter_list:
                                self.currency_counter[f'{follower}'] = watch_counter + 10

                                if watch_counter == 600:
                                    with open(self.filename, 'r') as load_file:
                                        minigame_json = json.load(load_file)

                                    self.currency_dict = minigame_json.get('currency', {})
                                    self.currency_dict[f'{follower}'] = self.currency_dict[f'{follower}'] + self.watch_reward

                                    with open(self.filename, 'w') as save_file:
                                        json.dump(minigame_json, save_file, indent=4)

                                    self.currency_counter[f'{follower}'] = 0

                    #log.log_info(f'[MINIGAME] currency_counter in loop: {self.currency_counter}')
                
                await asyncio.sleep(10)

            except Exception as err:
                error = f'[Twitch Minigame] (Balance) Error in currency_loop: {err}'
                log.log_error(error)

    
    # updates the follower and people watching the stream live list
    async def update_follower_chatter_list_loop(self):
        try:
            while True:
                self.is_live = request.get_streams()
                #log.log_info(f'[MINIGAME] is live: {self.is_live}')

                if not self.is_live:
                    self.currency_counter = {}
                    await asyncio.sleep(20)
                else:
                    self.follower_list = request.get_channel_followers()
                    self.chatter_list = request.get_channel_chatters()

                    for follower in self.follower_list:
                        if follower not in self.currency_counter and follower in self.chatter_list:
                            self.currency_counter[f'{follower}'] = 0

                #log.log_info(f'[MINIGAME] currency_counter in update: {self.currency_counter}')

                await asyncio.sleep(10)

        except Exception as err:
            error = f'[Twitch Minigame] (Balance) Error in update_follower_chatter_list: {err}'
            log.log_error(error)


    # returns the balance of the user
    async def get_balance(self, author, username):
        try:
            try:
                with open(self.filename, 'r') as load_file:
                    minigame_json = json.load(load_file)
                    currency_dict = minigame_json.get('currency', {})
            except:
                minigame_json = {'currency': {}}
                currency_dict = minigame_json['currency']

            try:
                balance = currency_dict[f'{username}']
                if username == author:
                    message = f'@{username} du hast {balance} stonks'
                else:
                    message = f'@{username} hat {balance} stonks'
            except:
                if username == author:
                    message = f'Du musst folgen um stonks fürs zuschauen zubekommen'
                else:
                    message = f'@{username} muss folgen um stonks fürs zuschauen zubekommen'

            return message

        except Exception as err:
            error = f'[Twitch Minigame] (Balance) Error in get_balance: {err}'
            log.log_error(error)

    
    # gives the top 5 users with the most stonks
    async def top_balance(self):
        try:
            try:
                with open(self.filename, 'r') as load_file:
                    minigame_json = json.load(load_file)
                    self.currency_dict = minigame_json.get('currency', {})
            except:
                minigame_json = {'currency': {}}
                self.currency_dict = minigame_json.get('currency', {})

            top_balance = sorted(self.currency_dict.items(), key=lambda x: x[1], reverse=True)[:5]

            top_balance_list = []
            top_balance_count = 0

            for username, balance in top_balance:
                top_balance_count += 1
                top_balance_list.append(f'#{top_balance_count} @{username} mit {balance} stonks')
            
            message = f'{top_balance_list[0]}, {top_balance_list[1]}, {top_balance_list[2]}, {top_balance_list[3]}, {top_balance_list[4]}'
            
            return message


        except Exception as err:
            error = f'[Twitch Minigame] (Balance) Error in top_balance: {err}'
            log.log_error(error)



# gamble class
class Gamble():
    def __init__(self):
        self.filename = 'json/twitch/minigame.json'
        self.bet = 0


    # randomly chooses if the user wins or lose
    async def gamble(self, bet: int, username: str):
        try:
            self.bet = bet
            win_or_lose = random.choice(['win', 'lose'])

            with open(self.filename, 'r') as save_file:
                minigame_json = json.load(save_file)
                currency_dict = minigame_json.get('currency', {})

            balance = currency_dict[f'{username}']

            if bet > balance:
                message = f'@{username} du hast nicht genügend stonks um diese Summe zu gamblen NotLikeThis'
                return message

            if win_or_lose == 'win':
                currency_dict[f'{username}'] = balance + bet
                message = f'@{username} du hast {bet} stonks gewonnen!'

            elif win_or_lose == 'lose':
                if bet != 0:
                    currency_dict[f'{username}'] = balance - bet

                message = f'@{username} du hast {bet} stonks verloren!'

            with open(self.filename, 'w') as load_file:
                json.dump(minigame_json, load_file, indent=4)

            return message
            
        except Exception as err:
            error = f'[Twitch Minigame] (Gamble) Error in gamble: {err}'
            log.log_error(error)



# stats class
class Stats():
    def __init__(self):
        self.filename = 'json/twitch/minigame.json'
        self.follower_list = None
        self.chatter_list = None
        self.stats_dict = None
        self.balance_dict = None
        self.cost_start = 10
        self.cost_multiplier = 1.5


    # on bot start it checks if there are new follower and initialize them to the stats dict
    async def initialize_stats(self):
        try:
            self.follower_list = request.get_channel_followers()
            self.chatter_list = request.get_channel_chatters()

            try:
                with open(self.filename, 'r') as load_file:
                    minigame_json = json.load(load_file)
                    self.stats_dict = minigame_json.get('stats', {})
            except:
                minigame_json['stats'] = {}
                self.stats_dict = minigame_json.get('stats', {})

            for follower in self.follower_list:
                if follower not in self.stats_dict:
                    self.stats_dict[f'{follower}'] = {'rizz': {'level': 0, 'last_cost': 0}, 'sigma': {'level': 0, 'last_cost': 0}, 'aura': {'level': 0, 'last_cost': 0}}

            with open(self.filename, 'w') as save_file:
                json.dump(minigame_json, save_file, indent=4)

            #log.log_info(f'[MINIGAME] log stats_dict in initialize: {self.stats_dict}')
        
        except Exception as err:
            error = f'[Twitch Minigame] (Balance) Error in initialize_stats: {err}'
            log.log_error(error)
        

    # loads the stats dict from the minigame.json
    def load_stats(self):
        try:
            try:
                with open(self.filename, 'r') as load_file:
                    self.minigame_json = json.load(load_file)
                    self.stats_dict = self.minigame_json.get('stats', {})
                    self.balance_dict = self.minigame_json.get('currency', {})
            except:
                self.minigame_json['stats'] = {}
                self.stats_dict = self.minigame_json.get('stats', {})

        except Exception as err:
            error = f'[Twitch Minigame] (Stats) Error in load_stats: {err}'
            log.log_error(error)


    # saves the stats dict to the minigame.json
    def save_stats(self):
        try:
            with open(self.filename, 'w') as save_file:
                json.dump(self.minigame_json, save_file, indent=4)

        except Exception as err:
            error = f'[Twitch Minigame] (Stats) Error in save_stats: {err}'
            log.log_error(error)

    
    # saves the new rizz count to the stats in the minigame.json
    def buy_rizz(self, username: str):
        try:
            self.load_stats()

            balance = self.balance_dict[f'{username}']

            stat = self.stats_dict[f'{username}']['rizz']

            level = stat['level']
            last_cost = stat['last_cost']

            if level >= 1:
                cost = int(last_cost) * self.cost_multiplier
                cost = int(Decimal(cost).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

            else:
                cost = self.cost_start

            if balance < cost:
                missing_stonks = cost - balance
                message = f'@{username} du hast nicht genügend stonks dafür. Du hast {balance} stonks und dir fehlen {missing_stonks} stonks louisd15Wah'
            
            else:
                new_balance = balance - cost
                new_level = level + 1

                next_cost = cost * self.cost_multiplier
                next_cost = int(Decimal(next_cost).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

                message = f'@{username} du hast jetzt {new_level} rizz! Das nächste Level kostet {next_cost} stonks Kreygasm'

                self.balance_dict[f'{username}'] = new_balance
                self.stats_dict[f'{username}']['rizz']['level'] = new_level
                self.stats_dict[f'{username}']['rizz']['last_cost'] = cost

                self.save_stats()
                
            return message

        except Exception as err:
            error = f'[Twitch Minigame] (Stats) Error in buy_rizz: {err}'
            log.log_error(error)


    # saves the new sigma count to the stats in the minigame.json
    def buy_sigma(self, username: str):
        try:
            self.load_stats()
            balance = self.balance_dict[f'{username}']

            stat = self.stats_dict[f'{username}']['sigma']
            level = stat['level']
            last_cost = int(stat['last_cost'])

            if level >= 1:
                cost = int(last_cost) * self.cost_multiplier
                cost = cost = int(Decimal(cost).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

            else:
                cost = self.cost_start

            if balance < cost:
                missing_stonks = cost - balance
                message = f'@{username} du hast nicht genügend stonks dafür. Du hast {balance} stonks und dir fehlen {missing_stonks} stonks louisd15Wah'
            
            else:
                new_balance = balance - cost
                new_level = level + 1

                next_cost = cost * self.cost_multiplier
                next_cost = int(Decimal(next_cost).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

                message = f'@{username} du hast jetzt {new_level} sigma! Das nächste Level kostet {next_cost} stonks Kreygasm'

                self.balance_dict[f'{username}'] = new_balance
                self.stats_dict[f'{username}']['sigma']['level'] = new_level
                self.stats_dict[f'{username}']['sigma']['last_cost'] = cost

                self.save_stats()
                
            return message
        
        except Exception as err:
            error = f'[Twitch Minigame] (Stats) Error in buy_sigma: {err}'
            log.log_error(error)


    # saves the new aura count to the stats in the minigame.json
    def buy_aura(self, username: str):
        try:
            self.load_stats()
            balance = self.balance_dict[f'{username}']

            stat = self.stats_dict[f'{username}']['aura']
            level = stat['level']
            last_cost = stat['last_cost']

            if level >= 1:
                cost = int(last_cost) * self.cost_multiplier
                cost = cost = int(Decimal(cost).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

            else:
                cost = self.cost_start

            if balance < cost:
                missing_stonks = cost - balance
                message = f'@{username} du hast nicht genügend stonks dafür. Du hast {balance} stonks und dir fehlen {missing_stonks} stonks louisd15Wah'
            
            else:
                new_balance = balance - cost
                new_level = level + 1

                next_cost = cost * self.cost_multiplier
                next_cost = int(Decimal(next_cost).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

                message = f'@{username} du hast jetzt {new_level} aura! Das nächste Level kostet {next_cost} stonks Kreygasm'

                self.balance_dict[f'{username}'] = new_balance
                self.stats_dict[f'{username}']['aura']['level'] = new_level
                self.stats_dict[f'{username}']['aura']['last_cost'] = cost

                self.save_stats()
                
            return message
        
        except Exception as err:
            error = f'[Twitch Minigame] (Stats) Error in buy_aura: {err}'
            log.log_error(error)


    # returns the stats from the user
    def get_stats(self, username: str):
        try:
            self.load_stats()
            stats = self.stats_dict[f'{username}']
            rizz_level = stats['rizz']['level']
            sigma_level = stats['sigma']['level']
            aura_level = stats['aura']['level']
            #log.log_info(f'Stats from {username}: {stats}')

            message = f'@{username} hat {rizz_level} rizz, {sigma_level} sigma und {aura_level} aura KomodoHype'

            return message

        except Exception as err:
            error = f'[Twitch Minigame] (Stats) Error in get_stats: {err}'
            log.log_error(error)




# async setup
async def async_setup():
    await asyncio.sleep(10)

    await Duel().duel_clear_dict()

    currency_system = Currency()
    await currency_system.initialize_currency()

    task1 = asyncio.create_task(currency_system.currency_loop())
    task2 = asyncio.create_task(currency_system.update_follower_chatter_list_loop())

    await Stats().initialize_stats()

    await asyncio.gather(task1, task2)


# setup
def setup():
    asyncio.run(async_setup())



if __name__ == '__main__':
    asyncio.run(setup())
