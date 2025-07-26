import random
import os
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
            print("🔄 Kartlar karıştırılıyor...")
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
    
    def is_soft(self) -> bool:
        """Soft el mi? (As'ın 11 değerinde olduğu el)"""
        total = 0
        aces = 0
        
        for card in self.cards:
            if card.rank == 'A':
                aces += 1
                total += 11
            else:
                total += card.get_value()
        
        # Eğer As'ları 1 yapmaya ihtiyaç yoksa soft
        return aces > 0 and total <= 21
    
    def is_bust(self) -> bool:
        """El 21'i geçti mi?"""
        return self.get_value() > 21
    
    def is_blackjack(self) -> bool:
        """Doğal blackjack mi? (2 kart ile 21)"""
        return len(self.cards) == 2 and self.get_value() == 21
    
    def clear(self):
        """Eli temizle"""
        self.cards = []
    
    def display(self, hide_first=False) -> str:
        """Eli görsel olarak göster"""
        if hide_first and len(self.cards) > 0:
            visible_cards = ["[?]"] + [str(card) for card in self.cards[1:]]
            return " ".join(visible_cards) + f" (Görünen: {sum(card.get_value() for card in self.cards[1:])})"
        else:
            return " ".join(str(card) for card in self.cards) + f" (Toplam: {self.get_value()})"

class InteractiveBlackjackGame:
    def __init__(self):
        self.deck = Deck(6)  # 6 deste
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.bet_amount = 100
        # GERÇEKÇİ CASINO KURALLARI
        self.blackjack_payout_ratio = 1.2  # 6:5 ödeme (120 birim)
        self.regular_win_payout = 100  # Normal kazanç (100 birim)
        
        # Oyun istatistikleri
        self.total_profit = 0
        self.games_played = 0
        self.games_won = 0
        self.games_lost = 0
        self.games_tied = 0
        self.blackjacks_hit = 0
    
    def clear_screen(self):
        """Ekranı temizle"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_game_state(self, hide_dealer_card=True):
        """Oyun durumunu göster"""
        print("=" * 60)
        print("🎰 GERÇEKÇİ CASINO BLACKJACK 🎰")
        print("=" * 60)
        print(f"💰 Toplam Kar/Zarar: {self.total_profit:+d} birim")
        print(f"🎮 Oyun Sayısı: {self.games_played} | Kazanılan: {self.games_won} | Kaybedilen: {self.games_lost} | Berabere: {self.games_tied}")
        if self.blackjacks_hit > 0:
            print(f"⚡ Blackjack Sayısı: {self.blackjacks_hit}")
        print("-" * 60)
        
        # Kasa eli
        print(f"🏠 KASA: {self.dealer_hand.display(hide_first=hide_dealer_card)}")
        
        # Oyuncu eli
        print(f"👤 SEN:  {self.player_hand.display()}")
        
        if self.player_hand.is_blackjack():
            print("⚡ BLACKJACK! 🎉")
        elif self.player_hand.is_bust():
            print("💥 PATLADIN! 😵")
        
        print("-" * 60)
    
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
    
    def get_player_action(self) -> str:
        """Oyuncudan aksiyon al"""
        while True:
            print("\n🎯 Ne yapmak istiyorsun?")
            print("  [H] Hit (Kart çek)")
            print("  [S] Stand (Dur)")
            print("  [Q] Quit (Çık)")
            
            action = input("\nSeçimin (H/S/Q): ").upper().strip()
            
            if action in ['H', 'S', 'Q']:
                return action
            else:
                print("❌ Geçersiz seçim! H, S veya Q yazın.")
    
    def dealer_play(self):
        """Kasa oynar (GERÇEKÇİ KURAL: soft 17'de kart çeker)"""
        print("\n🏠 Kasa oynuyor...")
        
        while True:
            dealer_value = self.dealer_hand.get_value()
            
            if dealer_value < 17:
                # 16 ve altında kart çek
                new_card = self.deck.deal_card()
                self.dealer_hand.add_card(new_card)
                print(f"   Kasa kart çekti: {new_card}")
            elif dealer_value == 17 and self.dealer_hand.is_soft():
                # SOFT 17'de kart çek (casino avantajı)
                new_card = self.deck.deal_card()
                self.dealer_hand.add_card(new_card)
                print(f"   Kasa soft 17'de kart çekti: {new_card}")
            else:
                # 17+ (hard) veya 18+ durur
                print(f"   Kasa durdu: {self.dealer_hand.get_value()}")
                break
            
            if self.dealer_hand.is_bust():
                print(f"   💥 Kasa patladı! ({self.dealer_hand.get_value()})")
                break
    
    def determine_winner(self) -> Tuple[str, int]:
        """Kazananı belirle ve kar/zarar miktarını döndür"""
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        # DOUBLE BUST KURALI: Oyuncu patladı mı?
        if self.player_hand.is_bust():
            return "dealer", -self.bet_amount
        
        # Kasa patladı
        if self.dealer_hand.is_bust():
            return "player", self.regular_win_payout
        
        # Blackjack kontrolleri
        player_bj = self.player_hand.is_blackjack()
        dealer_bj = self.dealer_hand.is_blackjack()
        
        if player_bj and dealer_bj:
            return "tie", 0
        elif player_bj:
            # GERÇEKÇİ KURAL: Blackjack 6:5 ödüyor (120 birim)
            self.blackjacks_hit += 1
            return "player", int(self.bet_amount * self.blackjack_payout_ratio)
        elif dealer_bj:
            return "dealer", -self.bet_amount
        
        # Normal karşılaştırma
        if player_value > dealer_value:
            return "player", self.regular_win_payout
        elif dealer_value > player_value:
            return "dealer", -self.bet_amount
        else:
            return "tie", 0
    
    def show_result(self, winner: str, profit: int):
        """Sonucu göster"""
        print("\n" + "=" * 60)
        print("🎯 SONUÇ")
        print("=" * 60)
        
        if winner == "player":
            if self.player_hand.is_blackjack():
                print("🎉 BLACKJACK KAZANDIN! ⚡")
                print(f"💰 Kazancın: +{profit} birim (6:5 ödeme)")
            else:
                print("🎉 KAZANDIN! 🏆")
                print(f"💰 Kazancın: +{profit} birim")
        elif winner == "dealer":
            if self.player_hand.is_bust():
                print("💥 PATLADIN! Kasa kazandı 😵")
            elif self.dealer_hand.is_blackjack():
                print("🏠 Kasa blackjack yaptı! 😔")
            else:
                print("🏠 Kasa kazandı 😔")
            print(f"💸 Kaybın: {profit} birim")
        else:
            print("🤝 BERABERE!")
            print("💰 Kar/Zarar: 0 birim")
        
        self.total_profit += profit
        print(f"📊 Toplam Kar/Zarar: {self.total_profit:+d} birim")
        print("=" * 60)
    
    def play_one_game(self) -> bool:
        """Bir oyun oyna. True döndürürse devam, False döndürürse çık"""
        self.games_played += 1
        
        # İlk kartları dağıt
        self.deal_initial_cards()
        
        # Oyun durumunu göster
        self.clear_screen()
        self.display_game_state(hide_dealer_card=True)
        
        # Blackjack kontrolü
        if self.player_hand.is_blackjack() or self.dealer_hand.is_blackjack():
            # Eğer birisi blackjack yaptıysa direkt sonuç
            winner, profit = self.determine_winner()
        else:
            # Oyuncu oynar
            while not self.player_hand.is_bust():
                action = self.get_player_action()
                
                if action == 'Q':
                    return False  # Oyundan çık
                elif action == 'H':
                    # Kart çek
                    new_card = self.deck.deal_card()
                    self.player_hand.add_card(new_card)
                    print(f"\n🎴 Çektiğin kart: {new_card}")
                    
                    # Durumu güncelle
                    self.clear_screen()
                    self.display_game_state(hide_dealer_card=True)
                    
                    if self.player_hand.is_bust():
                        break
                        
                elif action == 'S':
                    # Dur
                    break
            
            # Oyuncu patlamadıysa kasa oynar
            if not self.player_hand.is_bust():
                self.dealer_play()
            
            # Kazananı belirle
            winner, profit = self.determine_winner()
        
        # İstatistikleri güncelle
        if winner == "player":
            self.games_won += 1
        elif winner == "dealer":
            self.games_lost += 1
        else:
            self.games_tied += 1
        
        # Son durumu göster (kasa kartları açık)
        self.clear_screen()
        self.display_game_state(hide_dealer_card=False)
        
        # Sonucu göster
        self.show_result(winner, profit)
        
        # Devam etmek istiyor mu?
        input("\n⏎ Devam etmek için Enter'a bas...")
        return True
    
    def show_final_stats(self):
        """Final istatistiklerini göster"""
        self.clear_screen()
        print("=" * 60)
        print("🎰 OYUN BİTTİ - FİNAL İSTATİSTİKLERİ")
        print("=" * 60)
        print(f"🎮 Toplam Oyun: {self.games_played}")
        print(f"🏆 Kazanılan: {self.games_won}")
        print(f"😔 Kaybedilen: {self.games_lost}")
        print(f"🤝 Berabere: {self.games_tied}")
        if self.blackjacks_hit > 0:
            print(f"⚡ Blackjack Sayısı: {self.blackjacks_hit}")
        print("-" * 60)
        
        if self.games_played > 0:
            win_rate = (self.games_won / self.games_played) * 100
            print(f"📊 Kazanma Oranı: %{win_rate:.1f}")
            print(f"💰 Ortalama Oyun Başına: {self.total_profit/self.games_played:.1f} birim")
        
        print(f"💸 TOPLAM KAR/ZARAR: {self.total_profit:+d} birim")
        
        if self.total_profit > 0:
            print("🎉 Tebrikler! Casino'ya karşı kazandın!")
        elif self.total_profit < 0:
            print("😅 Casino kazandı... Ama iyi mücadele ettin!")
        else:
            print("🤝 Başabaş bitirdin!")
        
        print("=" * 60)
        print("🎰 CASINO KURALLARI HATIRLATMA:")
        print("   • Blackjack 6:5 ödedi (120 birim)")
        print("   • Kasa soft 17'de kart çekti")
        print("   • Double bust kuralı uygulandı")
        print("=" * 60)

def main():
    """Ana oyun döngüsü"""
    game = InteractiveBlackjackGame()
    
    # Hoş geldin mesajı
    game.clear_screen()
    print("=" * 60)
    print("🎰 GERÇEKÇİ CASINO BLACKJACK'E HOŞ GELDİN! 🎰")
    print("=" * 60)
    print("🏠 CASINO KURALLARI:")
    print("   • 6 deste kart kullanılıyor")
    print("   • Blackjack 6:5 ödüyor (120 birim)")
    print("   • Kasa soft 17'de kart çeker")
    print("   • Her oyun 100 birim bahis")
    print("   • Normal kazanç 100 birim")
    print("=" * 60)
    input("⏎ Oyuna başlamak için Enter'a bas...")
    
    # Oyun döngüsü
    try:
        while True:
            if not game.play_one_game():
                break
    except KeyboardInterrupt:
        print("\n\n👋 Oyundan çıkılıyor...")
    
    # Final istatistikleri
    game.show_final_stats()
    print("\n👋 Tekrar görüşmek üzere!")

if __name__ == "__main__":
    main() 