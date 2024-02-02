def gen_tb_dict(p, dur):
    """
    p (float): Probability server wins service point
    dur (int): Either 7 or 10 point tiebreak
    """
    ans = {}
    def tb_prop(p1, p2, server):
        """
        p1 (int): number of points that player1 has
        p2 (int): number of points that player2 has
        curr_server (int): # of the player serving (1 or 2)
        """
        #print(p1,p2)
        if (p1, p2, server) in ans:
            return
        if (p1 >= dur - 1) and (p2 >= dur-1):
            if (p1 == p2):
                ans[(p1, p2, server)] = 0.5
                return
            if (p1 == p2 + 1):
                if server == 1: # D + 1, 1
                    ans[(p1, p2, server)] = 0.5 + p/2
                else: # D + 1, 2
                    ans[(p1, p2, server)] = 1.0 - p/2
                return
            if (p1 + 1 == p2):
                if server == 1: # D - 1, 1
                    ans[(p1, p2, server)] = p/2
                else: # D - 1, 2
                    ans[(p1, p2, server)] = 0.5 - p/2
                return
            if p1 > p2:
                ans[(p1, p2, server)] = 1.0
                return
            ans[(p1, p2, server)] = 0.0
            return
        
        if (p1 == dur) and (p2 < dur - 1):
            ans[(p1, p2, server)] = 1.0
            return
        if (p1 < dur-1) and (p2 == dur):
            ans[(p1, p2, server)] = 0.0
            return
        
        n = server
        if (p1 + p2) % 2 == 0:
            n = (server % 2) + 1
        
        tb_prop(p1+1, p2, n)
        tb_prop(p1, p2+1, n)

        if (server == 1):
            ans[(p1, p2, server)] = p * ans[(p1 + 1, p2, n)] + (1-p) * ans[(p1, p2 + 1, n)]
        else:
            ans[(p1, p2, server)] = (1 - p) * ans[(p1 + 1, p2, n)] + p * ans[(p1, p2 + 1, n)]

    tb_prop(0,0,1)
    tb_prop(0,0,2)

    out = {}
    for key in ans.keys():
        out[str(key[0]) + "-" + str(key[1]) + "-" + str(key[2])] = ans[key]
    
    return out

def gen_set_dict(p):
    """
    p (float): probability server wins service point
    """
    ans = {}
    def in_set_prob(g1, g2, server):
        """
        g1 (int): number of games that player1 has
        g2 (int): number of games that player2 has
        curr_server (int): # of the player serving (1 or 2)
        """
        if (g1, g2) in ans:
            return
        if g1 == 7 and g2 == 5:
            ans[(g1, g2, server)] = 1.0
            return
        if g1 == 7 and g2 == 6:
            ans[(g1, g2, server)] = 1.0
            return
        if g1 == 5 and g2 == 7:
            ans[(g1, g2, server)] = 0.0
            return
        if g1 == 6 and g2 == 7:
            ans[(g1, g2, server)] = 0.0
            return
        if g1 == 6 and g2 < 5:
            ans[(g1, g2, server)] = 1.0
            return
        if g1 < 5 and g2 == 6:
            ans[(g1, g2, server)] = 0.0
            return
        if g1 == 6 and g2 == 6:
            ans[(g1, g2, server)] = 0.5
            return
        n = (server % 2) + 1
        in_set_prob(g1 + 1, g2, n)
        in_set_prob(g1, g2 + 1, n)
        w = 0
        if server == 1:
            w = gen_game_dict(p)["0-0"] # odds p1 holds serve
        else:
            w = gen_game_dict(1-p)["0-0"] # odds p1 breaks serve
        ans[(g1, g2, server)] = w * ans[(g1 + 1, g2, n)] + (1 - w) * ans[(g1, g2 + 1, n)]

    in_set_prob(0, 0, 1)
    in_set_prob(0, 0, 2)
    ans[(7,6,1)] = 1.0
    ans[(7,6,2)] = 1.0
    ans[(6,7,1)] = 0.0
    ans[(6,7,2)] = 0.0

    out = {}
    for key in ans.keys():
        out[str(key[0]) + "-" + str(key[1]) + "-" + str(key[2])] = ans[key]
    
    return out


def gen_game_dict(p):
    d = p**2/(1-2*p*(1-p))
    ans = {}
    ans[(3,3)] = d
    ans[(4,4)] = d
    ans[(4,3)] = p + (1-p)*d
    ans[(3,4)] = p*d
    
    def in_game_prob(points1, points2):
        """
        Probability that player1 wins this game
        points1 (int): 0 -> 0, 1 -> 15, 2 -> 30, 3 -> 40, 4 -> AD, number of points that player1 has
        points2 (int): 0 -> 0, 1 -> 15, 2 -> 30, 3 -> 40, 4 -> AD, number of points that player2 has
        p (float): probability that player1 wins a point in this game
        """
        if (points1 > 4) and (points2 == 3):
            ans[(points1, points2)] = 1.0
            return
        if (points1 == 3) and (points2 > 4):
            ans[(points1, points2)] = 0.0
            return
        if (points1 == 4) and (points2 < 3):
            ans[(points1, points2)] = 1.0
            return
        if (points1 < 3) and (points2 == 4):
            ans[(points1, points2)] = 0.0
            return
        
        if (points1 == 4) and (points2 == 4):
            points1 = 3
            points2 = 3
        
        if (points1, points2) in ans:
            return
        
        in_game_prob(points1+1, points2)
        in_game_prob(points1, points2+1)
        

        ans[(points1, points2)] = p * ans[(points1 + 1, points2)] + (1 - p ) * ans[(points1, points2 + 1)]
    
    in_game_prob(0, 0)
    out = {}
    L = ["0", "15", "30", "40", "AD"]
    for key in ans.keys():
        out[L[key[0]] + "-" + L[key[1]]] = ans[key]
    
    return out

#print(gen_set_dict(0.60))

def win_prob(sets, games, points):
    """
    sets (str): 'X-Y' where X is player1 sets, Y is player2 sets
    games (str): 'X-Y' where X is player1 games, Y is player2 games
    points (str): 'X-Y' where X is player1 points, Y is player2 points

    The probability that player1 wins this match
    """
    sets_hardcoded = {
        "0-0": 0.5,
        "0-1": 0.3125,
        "1-0": 0.6875,
        "1-1": 0.5,
        "2-0": 0.875,
        "0-2": 0.125,
        "2-1": 0.75,
        "1-2": 0.25,
        "2-2": 0.5,
        "3-0": 1,
        "3-1": 1,
        "3-2": 1,
        "0-3": 0,
        "1-3": 0,
        "2-3": 0
    }

    games_hardcoded = {
        "0-0": 0.5,
        "1-0": 0.623046875,
        "0-1": 0.376953125,
        "2-0": 0.74609375,
        "0-2": 0.25390625,
        "1-1": 0.5,
        "3-0": 0.85546875,
        "2-1": 0.63671875,
        "1-2": 0.36328125,
        "0-3": 0.14453125,
        "4-0": 0.9375,
        "3-1": 0.7734375,
        "2-2": 0.5,
        "1-3": 0.2265625,
        "0-4": 0.0625,
        "5-0": 0.984375,
        "4-1": 0.890625,
        "3-2": 0.65625,
        "2-3": 0.34375,
        "1-4": 0.109375,
        "0-5": 0.015625,
        "5-1": 0.96875,
        "4-2": 0.8125,
        "3-3": 0.5,
        "2-4": 0.1875,
        "1-5": 0.03125,
        "5-2": 0.9375,
        "4-3": 0.6875,
        "3-4": 0.3125,
        "2-5": 0.0625,
        "5-3": 0.875,
        "4-4": 0.5,
        "3-5": 0.125,
        "5-4": 0.75,
        "4-5": 0.25,
        "5-5": 0.5,
        "6-5": 0.75,
        "5-6": 0.25,
        "6-6": 0.5,
        "6-0": 1,
        "6-1": 1,
        "6-2": 1,
        "6-3": 1,
        "6-4": 1,
        "7-5": 1,
        "5-7": 0,
        "4-6": 0,
        "3-6": 0,
        "2-6": 0,
        "1-6": 0,
        "0-6": 0,
        "7-6": 1,
        "6-7": 0
    }

    tb_hardcoded = {
        '7-0': 1.0,
        '7-1': 1.0,
        '7-2': 1.0,
        '7-3': 1.0,
        '7-4': 1.0,
        '7-5': 1.0,
        '7-6': 1.0,
        '6-7': 0.0,
        '6-6': 0.5,
        '6-5': 0.75,
        '6-4': 0.875,
        '6-3': 0.9375,
        '6-2': 0.96875,
        '6-1': 0.984375,
        '6-0': 0.9921875,
        '5-7': 0.0,
        '5-6': 0.25,
        '5-5': 0.5,
        '5-4': 0.6875,
        '5-3': 0.8125,
        '5-2': 0.890625,
        '5-1': 0.9375,
        '5-0': 0.96484375,
        '4-7': 0.0,
        '4-6': 0.125,
        '4-5': 0.3125,
        '4-4': 0.5,
        '4-3': 0.65625,
        '4-2': 0.7734375,
        '4-1': 0.85546875,
        '4-0': 0.91015625,
        '3-7': 0.0,
        '3-6': 0.0625,
        '3-5': 0.1875,
        '3-4': 0.34375,
        '3-3': 0.5,
        '3-2': 0.63671875,
        '3-1': 0.74609375,
        '3-0': 0.828125,
        '2-7': 0.0,
        '2-6': 0.03125,
        '2-5': 0.109375,
        '2-4': 0.2265625,
        '2-3': 0.36328125,
        '2-2': 0.5,
        '2-1': 0.623046875,
        '2-0': 0.7255859375,
        '1-7': 0.0,
        '1-6': 0.015625,
        '1-5': 0.0625,
        '1-4': 0.14453125,
        '1-3': 0.25390625,
        '1-2': 0.376953125,
        '1-1': 0.5,
        '1-0': 0.61279296875,
        '0-7': 0.0,
        '0-6': 0.0078125,
        '0-5': 0.03515625,
        '0-4': 0.08984375,
        '0-3': 0.171875,
        '0-2': 0.2744140625,
        '0-1': 0.38720703125,
        '0-0': 0.5
    }

    tptb_hardcoded = {
        '10-0': 1.0,
        '10-1': 1.0,
        '10-2': 1.0,
        '10-3': 1.0,
        '10-4': 1.0,
        '10-5': 1.0,
        '10-6': 1.0,
        '10-7': 1.0,
        '10-8': 1.0,
        '10-9': 1.0,
        '9-10': 0.0,
        '9-9': 0.5,
        '9-8': 0.75,
        '9-7': 0.875,
        '9-6': 0.9375,
        '9-5': 0.96875,
        '9-4': 0.984375,
        '9-3': 0.9921875,
        '9-2': 0.99609375,
        '9-1': 0.998046875,
        '9-0': 0.9990234375,
        '8-10': 0.0,
        '8-9': 0.25,
        '8-8': 0.5,
        '8-7': 0.6875,
        '8-6': 0.8125,
        '8-5': 0.890625,
        '8-4': 0.9375,
        '8-3': 0.96484375,
        '8-2': 0.98046875,
        '8-1': 0.9892578125,
        '8-0': 0.994140625,
        '7-10': 0.0,
        '7-9': 0.125,
        '7-8': 0.3125,
        '7-7': 0.5,
        '7-6': 0.65625,
        '7-5': 0.7734375,
        '7-4': 0.85546875,
        '7-3': 0.91015625,
        '7-2': 0.9453125,
        '7-1': 0.96728515625,
        '7-0': 0.980712890625,
        '6-10': 0.0,
        '6-9': 0.0625,
        '6-8': 0.1875,
        '6-7': 0.34375,
        '6-6': 0.5,
        '6-5': 0.63671875,
        '6-4': 0.74609375,
        '6-3': 0.828125,
        '6-2': 0.88671875,
        '6-1': 0.927001953125,
        '6-0': 0.953857421875,
        '5-10': 0.0,
        '5-9': 0.03125,
        '5-8': 0.109375,
        '5-7': 0.2265625,
        '5-6': 0.36328125,
        '5-5': 0.5,
        '5-4': 0.623046875,
        '5-3': 0.7255859375,
        '5-2': 0.80615234375,
        '5-1': 0.8665771484375,
        '5-0': 0.91021728515625,
        '4-10': 0.0,
        '4-9': 0.015625,
        '4-8': 0.0625,
        '4-7': 0.14453125,
        '4-6': 0.25390625,
        '4-5': 0.376953125,
        '4-4': 0.5,
        '4-3': 0.61279296875,
        '4-2': 0.70947265625,
        '4-1': 0.78802490234375,
        '4-0': 0.84912109375,
        '3-10': 0.0,
        '3-9': 0.0078125,
        '3-8': 0.03515625,
        '3-7': 0.08984375,
        '3-6': 0.171875,
        '3-5': 0.2744140625,
        '3-4': 0.38720703125,
        '3-3': 0.5,
        '3-2': 0.604736328125,
        '3-1': 0.696380615234375,
        '3-0': 0.7727508544921875,
        '2-10': 0.0,
        '2-9': 0.00390625,
        '2-8': 0.01953125,
        '2-7': 0.0546875,
        '2-6': 0.11328125,
        '2-5': 0.19384765625,
        '2-4': 0.29052734375,
        '2-3': 0.395263671875,
        '2-2': 0.5,
        '2-1': 0.5981903076171875,
        '2-0': 0.6854705810546875,
        '1-10': 0.0,
        '1-9': 0.001953125,
        '1-8': 0.0107421875,
        '1-7': 0.03271484375,
        '1-6': 0.072998046875,
        '1-5': 0.1334228515625,
        '1-4': 0.21197509765625,
        '1-3': 0.303619384765625,
        '1-2': 0.4018096923828125,
        '1-1': 0.5,
        '1-0': 0.5927352905273438,
        '0-10': 0.0,
        '0-9': 0.0009765625,
        '0-8': 0.005859375,
        '0-7': 0.019287109375,
        '0-6': 0.046142578125,
        '0-5': 0.08978271484375,
        '0-4': 0.15087890625,
        '0-3': 0.2272491455078125,
        '0-2': 0.3145294189453125,
        '0-1': 0.40726470947265625,
        '0-0': 0.5
    }

    points_hardcoded = {
        "0-0": 0.5,
        "15-0": 0.65625,
        "0-15": 0.34375,
        "15-15": 0.5,
        "15-30": 0.1875,
        "30-15": 0.8125,
        "30-0": 0.875,
        "0-30": 0.125,
        "30-30": 0.5,
        "40-0": 0.9375,
        "0-40": 0.0625,
        "40-15": 0.875,
        "15-40": 0.125,
        "40-30": 0.75,
        "30-40": 0.25,
        "40-40": 0.5,
        "AD-40": 0.75,
        "40-AD": 0.25
    }
    s1, s2 = map(int, sets.split("-"))
    

    

    if games == None: # we are only considering sets
        return sets_hardcoded[sets]
    elif points == None: # we are only considering sets and games
        return games_hardcoded[games] * win_prob(str(s1 + 1) + "-" + str(s2), None, None) + (1-games_hardcoded[games]) * win_prob(str(s1) + "-" + str(s2 + 1), None, None)

    g1, g2 = map(int, games.split("-"))
    p1, p2 = points.split("-")
    # Edge cases
    tiebreak = (g1 == 6) and (g2 == 6) 
    wb2 = tiebreak and (int(p1) >= 6) and (int(p2) >= 6)
    ten_point_tb = tiebreak and (s1 == 2) and (s2 == 2)
    tpwb2 = ten_point_tb and (int(p1) >= 9) and (int(p2) >= 9)
    val = 0
    if (ten_point_tb):
        if (tpwb2):
            if p1 > p2:
                val = 0.75
            elif p1 == p2:
                val = 0.5
            else:
                val = 0.25
        else:
            val = tptb_hardcoded[points]

    elif (tiebreak):
        if (wb2):
            if p1 > p2:
                val = 0.75
            elif p1 == p2:
                val = 0.5
            else:
                val = 0.25
        else:
            val = tb_hardcoded[points]
    else:
        val = points_hardcoded[points]

    return val * win_prob(sets, str(g1 + 1) + "-" + str(g2), None) + (1-val) * win_prob(sets, str(g1) + "-" + str(g2+1), None)


class Metric_Finder():
    def __init__(self, p):
        self.p = p
        self.games_dict = gen_set_dict(p)
        self.tb_dict_7 = gen_tb_dict(p, 7)
        self.tb_dict_10 = gen_tb_dict(p, 10)
        self.game_dict_serving = gen_game_dict(p)
        self.game_dict_receiving = gen_game_dict(1-p)

    def find_metric(self, sets, games, points, curr_server): 
        def aheadness_metric(sets, games, points, curr_server):
            """
            sets (str): 'X-Y' where X is player1 sets, Y is player2 sets
            games (str): 'X-Y' where X is player1 games, Y is player2 games
            points (str): 'X-Y' where X is player1 points, Y is player2 points
            curr_server (int): 1 if player1 serving, 2 if player2 serving
            p (float): 0.0-1.0, probability that the serving player wins a service game

            The probability that player1 wins this match
            """
            sets_hardcoded = {
                "0-0": 0.5,
                "0-1": 0.3125,
                "1-0": 0.6875,
                "1-1": 0.5,
                "2-0": 0.875,
                "0-2": 0.125,
                "2-1": 0.75,
                "1-2": 0.25,
                "2-2": 0.5,
                "3-0": 1,
                "3-1": 1,
                "3-2": 1,
                "0-3": 0,
                "1-3": 0,
                "2-3": 0
            }
            
            if games == None:
                return sets_hardcoded[sets]
            if points == None:
                s1, s2 = map(int, sets.split("-"))
                g1, g2 = map(int, games.split("-"))
                
                return self.games_dict[games + "-" + str(curr_server)] * aheadness_metric(str(s1 + 1) + "-" + str(s2), None, None, None) + (1 - self.games_dict[games + "-" + str(curr_server)]) * aheadness_metric(str(s1) + "-" + str(s2 + 1), None, None, None)
            
            s1, s2 = map(int, sets.split("-"))
            g1, g2 = map(int, games.split("-"))
            p1, p2 = points.split("-")
            tiebreak = (g1 == 6) and (g2 == 6) 
            ten_point_tb = tiebreak and (s1 == 2) and (s2 == 2)
            val = -1
            if tiebreak:
                dur = 7
                if (ten_point_tb):
                    dur = 10
                p1 = int(p1)
                p2 = int(p2)
                if (p1 >= dur - 1) and (p2 >= dur-1):
                    if (p1 == p2):
                        val = 0.5
                    elif (p1 == p2 + 1):
                        if curr_server == 1: # D + 1, 1
                            val = 0.5 + self.p/2
                        else: # D + 1, 2
                            val = 1.0 - self.p/2
                    elif (p1 + 1 == p2):
                        if curr_server == 1: # D - 1, 1
                            val = self.p/2
                        else: # D - 1, 2
                            val = 0.5 - self.p/2
                    else:
                        if p1 > p2:
                            val = 1.0
                        else:
                            val = 0.0
                
                if (p1 == dur) and (p2 < dur - 1):
                    val = 1.0
                elif (p1 < dur-1) and (p2 == dur):
                    val = 0.0
                
                if (val == -1):
                    
                    #print(points)
                    if dur == 7:
                        val = self.tb_dict_7[points + "-" + str(curr_server)]
                    else:
                        val = self.tb_dict_10[points + "-" + str(curr_server)]
                    #print("it works")
            else:
                game_dict = None
                if curr_server == 1:
                    game_dict = self.game_dict_serving # p1 service game
                else:
                    game_dict = self.game_dict_receiving # p1 receiving game
                #print(game_dict)
                val = game_dict[points]

            return val * aheadness_metric(sets, str(g1 + 1) + "-" + str(g2), None, (curr_server % 2) + 1) + (1-val) * aheadness_metric(sets, str(g1) + "-" + str(g2+1), None, (curr_server % 2) + 1)
        return aheadness_metric(sets, games, points, curr_server)

met = Metric_Finder(0.6)
print(met.find_metric("0-0","0-0","15-0", 1))
