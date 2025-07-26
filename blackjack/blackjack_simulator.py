import random
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
from enum import Enum

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Card:
    def __init__(self, rank: str, suit: Suit):
        self.rank = rank
        self.suit = suit
    
    def get_value(self) -> int:
        """Kartın blackjack değerini döndürür"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # As'ın değeri context'e göre ayarlanacak
        else:
            return int(self.rank)
    
    def __str__(self):
        return f"{self.rank}{self.suit.value}"

class Deck:
    def __init__(self, num_decks: int = 6):
        self.num_decks = num_decks
        self.cards = []
        self.reset_deck()
    
    def reset_deck(self):
        """Desteyi sıfırla ve karıştır"""
        self.cards = []
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        for _ in range(self.num_decks):
            for suit in Suit:
                for rank in ranks:
                    self.cards.append(Card(rank, suit))
        
        random.shuffle(self.cards)
    
    def deal_card(self) -> Card:
        """Bir kart çek"""
        if len(self.cards) < 20:  # Deste biterse yenile
            self.reset_deck()
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards: List[Card] = []
    
    def add_card(self, card: Card):
        """Ele kart ekle"""
        self.cards.append(card)
    
    def get_value(self) -> int:
        """Elin toplam değerini hesapla (As'ları optimize et)"""
        total = 0
        aces = 0
        
        for card in self.cards:
            if card.rank == 'A':
                aces += 1
                total += 11
            else:
                total += card.get_value()
        
        # As'ları optimize et (11'den 1'e çevir)
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        
        return total
    
    def is_bust(self) -> bool:
        """El 21'i geçti mi?"""
        return self.get_value() > 21
    
    def is_blackjack(self) -> bool:
        """Doğal blackjack mi? (2 kart ile 21)"""
        return len(self.cards) == 2 and self.get_value() == 21
    
    def clear(self):
        """Eli temizle"""
        self.cards = []
    
    def __str__(self):
        return f"[{', '.join(str(card) for card in self.cards)}] = {self.get_value()}"

class BlackjackGame:
    def __init__(self):
        self.deck = Deck(6)  # 6 deste
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.bet_amount = 100
        self.win_amount = 150
    
    def deal_initial_cards(self):
        """İlk kartları dağıt"""
        self.player_hand.clear()
        self.dealer_hand.clear()
        
        # Oyuncuya 2 kart
        self.player_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        
        # Kasaya 2 kart (biri kapalı)
        self.dealer_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
    
    def player_should_hit(self) -> bool:
        """Oyuncu kart çekmeli mi? (rastgele risk alma stratejisi)"""
        player_value = self.player_hand.get_value()
        
        if player_value < 12:
            return True  # 11 ve altında her zaman çek
        elif player_value >= 21:
            return False  # 21 ve üstünde çekme
        elif player_value <= 16:
            # 12-16 arası: %80 ihtimalle çek
            return random.random() < 0.8
        elif player_value == 17:
            # 17'de risk al: %20 ihtimalle çek
            return random.random() < 0.2
        else:
            # 18-20 arası: %5 ihtimalle çek (çok nadir risk)
            return random.random() < 0.05
    
    def dealer_play(self):
        """Kasa oynar (17'de durur)"""
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
    
    def determine_winner(self) -> Tuple[str, int]:
        """Kazananı belirle ve kar/zarar miktarını döndür"""
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        # Oyuncu patladı
        if self.player_hand.is_bust():
            return "dealer", -self.bet_amount
        
        # Kasa patladı
        if self.dealer_hand.is_bust():
            return "player", self.win_amount
        
        # Blackjack kontrolleri
        player_bj = self.player_hand.is_blackjack()
        dealer_bj = self.dealer_hand.is_blackjack()
        
        if player_bj and dealer_bj:
            return "tie", 0
        elif player_bj:
            return "player", self.win_amount
        elif dealer_bj:
            return "dealer", -self.bet_amount
        
        # Normal karşılaştırma
        if player_value > dealer_value:
            return "player", self.win_amount
        elif dealer_value > player_value:
            return "dealer", -self.bet_amount
        else:
            return "tie", 0
    
    def play_one_game(self) -> Tuple[str, int]:
        """Bir oyun oyna ve sonucu döndür"""
        self.deal_initial_cards()
        
        # Oyuncu oynar
        while self.player_should_hit() and not self.player_hand.is_bust():
            self.player_hand.add_card(self.deck.deal_card())
        
        # Oyuncu patlamadıysa kasa oynar
        if not self.player_hand.is_bust():
            self.dealer_play()
        
        return self.determine_winner()

class BlackjackSimulator:
    def __init__(self):
        self.game = BlackjackGame()
        self.results = []
        self.cumulative_profit = []
    
    def run_simulation(self, num_games: int = 10000):
        """Simülasyonu çalıştır"""
        print(f"{num_games} oyun simülasyonu başlıyor...")
        
        total_profit = 0
        
        for i in range(num_games):
            winner, profit = self.game.play_one_game()
            total_profit += profit
            
            self.results.append({
                'game_number': i + 1,
                'winner': winner,
                'profit': profit,
                'cumulative_profit': total_profit
            })
            
            self.cumulative_profit.append(total_profit)
            
            # Her 1000 oyunda bir rapor
            if (i + 1) % 1000 == 0:
                print(f"{i + 1} oyun tamamlandı. Toplam kar/zarar: {total_profit}")
        
        print(f"Simülasyon tamamlandı! Toplam kar/zarar: {total_profit}")
        return self.results
    
    def plot_results(self):
        """Sonuçları grafikle göster"""
        # Her 1000 oyun için kar/zarar
        profits_per_1000 = []
        game_ranges = []
        
        for i in range(0, len(self.cumulative_profit), 1000):
            start_profit = self.cumulative_profit[i-1] if i > 0 else 0
            end_profit = self.cumulative_profit[min(i+999, len(self.cumulative_profit)-1)]
            profits_per_1000.append(end_profit - start_profit)
            game_ranges.append(f"{i+1}-{min(i+1000, len(self.cumulative_profit))}")
        
        # Grafik oluştur
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Her 1000 oyun için kar/zarar
        ax1.bar(range(len(profits_per_1000)), profits_per_1000, 
                color=['green' if p > 0 else 'red' for p in profits_per_1000])
        ax1.set_title('Her 1000 Oyun İçin Kar/Zarar Dağılımı')
        ax1.set_xlabel('Oyun Aralığı')
        ax1.set_ylabel('Kar/Zarar (Birim)')
        ax1.set_xticks(range(len(game_ranges)))
        ax1.set_xticklabels(game_ranges, rotation=45)
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        # Kümülatif kar/zarar
        ax2.plot(range(1, len(self.cumulative_profit) + 1), self.cumulative_profit, 
                 color='blue', linewidth=1)
        ax2.set_title('Kümülatif Kar/Zarar Eğrisi')
        ax2.set_xlabel('Oyun Sayısı')
        ax2.set_ylabel('Toplam Kar/Zarar (Birim)')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        plt.tight_layout()
        plt.show()
        
        # İstatistikler yazdır
        self.print_statistics()
    
    def print_statistics(self):
        """Detaylı istatistikleri yazdır"""
        total_games = len(self.results)
        wins = sum(1 for r in self.results if r['winner'] == 'player')
        losses = sum(1 for r in self.results if r['winner'] == 'dealer')
        ties = sum(1 for r in self.results if r['winner'] == 'tie')
        
        win_rate = (wins / total_games) * 100
        loss_rate = (losses / total_games) * 100
        tie_rate = (ties / total_games) * 100
        
        total_profit = self.cumulative_profit[-1]
        
        print("\n" + "="*50)
        print("BLACKJACK SİMÜLASYON İSTATİSTİKLERİ")
        print("="*50)
        print(f"Toplam Oyun Sayısı: {total_games}")
        print(f"Kazanılan Oyunlar: {wins} (%{win_rate:.1f})")
        print(f"Kaybedilen Oyunlar: {losses} (%{loss_rate:.1f})")
        print(f"Berabere Oyunlar: {ties} (%{tie_rate:.1f})")
        print(f"Toplam Kar/Zarar: {total_profit} birim")
        print(f"Ortalama Oyun Başına Kar/Zarar: {total_profit/total_games:.2f} birim")
        print("="*50)

if __name__ == "__main__":
    # Simülatörü çalıştır
    simulator = BlackjackSimulator()
    simulator.run_simulation(10000)
    simulator.plot_results() 