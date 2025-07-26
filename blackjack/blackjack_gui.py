import pygame
import random
import sys
from typing import List, Tuple
from enum import Enum

# Pygame başlatma
pygame.init()

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 100, 0)
LIGHT_GRAY = (200, 200, 200)

# Ekran boyutları
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

# Kart boyutları
CARD_WIDTH = 100
CARD_HEIGHT = 140

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
            return 11
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
        if len(self.cards) < 20:
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
        """Soft el mi?"""
        total = 0
        aces = 0
        
        for card in self.cards:
            if card.rank == 'A':
                aces += 1
                total += 11
            else:
                total += card.get_value()
        
        return aces > 0 and total <= 21
    
    def is_bust(self) -> bool:
        """El 21'i geçti mi?"""
        return self.get_value() > 21
    
    def is_blackjack(self) -> bool:
        """Doğal blackjack mi?"""
        return len(self.cards) == 2 and self.get_value() == 21
    
    def clear(self):
        """Eli temizle"""
        self.cards = []

class BlackjackGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎰 Gerçekçi Casino Blackjack")
        self.clock = pygame.time.Clock()
        
        # Fontlar - Unicode destekli fontlar kullan
        try:
            # Sistem fontunu dene (Unicode destekli)
            self.font_large = pygame.font.SysFont('arial', 48, bold=True)
            self.font_medium = pygame.font.SysFont('arial', 32)
            self.font_small = pygame.font.SysFont('arial', 22)
            self.font_card = pygame.font.SysFont('arial', 28, bold=True)  # Kartlar için özel font
        except:
            # Fallback - varsayılan font
            self.font_large = pygame.font.Font(None, 56)
            self.font_medium = pygame.font.Font(None, 42)
            self.font_small = pygame.font.Font(None, 28)
            self.font_card = pygame.font.Font(None, 36)
        
        # Oyun durumu
        self.deck = Deck(6)
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.bet_amount = 100
        self.blackjack_payout_ratio = 1.2  # 6:5 ödeme
        self.regular_win_payout = 100
        
        # İstatistikler
        self.total_profit = 0
        self.games_played = 0
        self.games_won = 0
        self.games_lost = 0
        self.games_tied = 0
        self.blackjacks_hit = 0
        
        # Oyun durumu
        self.game_state = "menu"  # menu, playing, game_over, result
        self.hide_dealer_card = True
        self.message = ""
        self.result_message = ""
        
        # Butonlar
        self.buttons = {}
        self.create_buttons()
    
    def create_buttons(self):
        """Butonları oluştur"""
        # Ana menü butonları
        self.buttons["start"] = pygame.Rect(SCREEN_WIDTH//2 - 120, 450, 240, 70)
        self.buttons["quit"] = pygame.Rect(SCREEN_WIDTH//2 - 120, 540, 240, 70)
        
        # Oyun butonları - alt merkeze yerleştir, daha büyük boyutlar
        button_width = 160  # 140'tan 160'a artırıldı
        button_height = 70  # 60'tan 70'e artırıldı
        button_spacing = 25
        total_width = 4 * button_width + 3 * button_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        button_y = SCREEN_HEIGHT - 120  # Biraz daha yukarı
        
        self.buttons["hit"] = pygame.Rect(start_x, button_y, button_width, button_height)
        self.buttons["stand"] = pygame.Rect(start_x + button_width + button_spacing, button_y, button_width, button_height)
        self.buttons["new_game"] = pygame.Rect(start_x + 2 * (button_width + button_spacing), button_y, button_width, button_height)
        self.buttons["exit"] = pygame.Rect(start_x + 3 * (button_width + button_spacing), button_y, button_width, button_height)
    
    def draw_card(self, card: Card, x: int, y: int, hidden: bool = False):
        """Kart çiz"""
        # Kart arka planı
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        
        if hidden:
            # Kapalı kart (mavi arka plan)
            pygame.draw.rect(self.screen, BLUE, card_rect)
            pygame.draw.rect(self.screen, WHITE, card_rect, 2)
            
            # Kart deseni
            for i in range(3):
                for j in range(5):
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x + 15 + i * 25, y + 15 + j * 20), 3)
        else:
            # Açık kart (beyaz arka plan)
            pygame.draw.rect(self.screen, WHITE, card_rect)
            pygame.draw.rect(self.screen, BLACK, card_rect, 2)
            
            # Kart rengi (kırmızı veya siyah)
            color = RED if card.suit in [Suit.HEARTS, Suit.DIAMONDS] else BLACK
            
            # Rank (sol üst) - daha büyük font
            rank_text = self.font_card.render(card.rank, True, color)
            self.screen.blit(rank_text, (x + 8, y + 8))
            
            # Suit (sol üst, rank'in altında) - özel font ile
            suit_text = self.font_card.render(card.suit.value, True, color)
            self.screen.blit(suit_text, (x + 8, y + 35))
            
            # Orta büyük suit - daha büyük
            big_suit_font = pygame.font.SysFont('arial', 40, bold=True)
            try:
                big_suit = big_suit_font.render(card.suit.value, True, color)
            except:
                big_suit = self.font_large.render(card.suit.value, True, color)
            suit_rect = big_suit.get_rect(center=(x + CARD_WIDTH//2, y + CARD_HEIGHT//2))
            self.screen.blit(big_suit, suit_rect)
            
            # Rank (sağ alt, ters) - daha büyük
            rank_text_bottom = pygame.transform.rotate(
                self.font_card.render(card.rank, True, color), 180)
            self.screen.blit(rank_text_bottom, 
                           (x + CARD_WIDTH - 30, y + CARD_HEIGHT - 40))
            
            # Suit (sağ alt, ters) - daha büyük
            suit_text_bottom = pygame.transform.rotate(
                self.font_card.render(card.suit.value, True, color), 180)
            self.screen.blit(suit_text_bottom, 
                           (x + CARD_WIDTH - 30, y + CARD_HEIGHT - 65))
    
    def draw_hand(self, hand: Hand, x: int, y: int, hide_first: bool = False):
        """El çiz - kartlar arası mesafeyi artır"""
        card_spacing = 120  # Kartlar arası mesafe artırıldı
        for i, card in enumerate(hand.cards):
            card_x = x + i * card_spacing
            hidden = hide_first and i == 0
            self.draw_card(card, card_x, y, hidden)
    
    def draw_button(self, button_rect: pygame.Rect, text: str, color: tuple = LIGHT_GRAY, 
                   text_color: tuple = BLACK, enabled: bool = True):
        """Buton çiz"""
        if not enabled:
            color = GRAY
            text_color = WHITE
        
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, BLACK, button_rect, 2)
        
        # Buton yazısı için daha küçük font kullan
        button_font = pygame.font.SysFont('arial', 24, bold=True)
        try:
            button_text = button_font.render(text, True, text_color)
        except:
            button_text = self.font_small.render(text, True, text_color)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
    
    def draw_menu(self):
        """Ana menü çiz"""
        self.screen.fill(DARK_GREEN)
        
        # Başlık
        title = self.font_large.render("*** GERCEKCI CASINO BLACKJACK ***", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 180))
        self.screen.blit(title, title_rect)
        
        # Kurallar
        rules = [
            ">>> CASINO KURALLARI:",
            "- 6 deste kart kullaniliyor",
            "- Blackjack 6:5 oduyor (120 birim)",
            "- Kasa soft 17'de kart ceker",
            "- Her oyun 100 birim bahis",
            "- Normal kazanc 100 birim"
        ]
        
        for i, rule in enumerate(rules):
            color = GOLD if i == 0 else WHITE
            rule_text = self.font_small.render(rule, True, color)
            rule_rect = rule_text.get_rect(center=(SCREEN_WIDTH//2, 260 + i * 30))
            self.screen.blit(rule_text, rule_rect)
        
        # Butonlar
        self.draw_button(self.buttons["start"], "OYUNA BAŞLA", GREEN, WHITE)
        self.draw_button(self.buttons["quit"], "ÇIKIŞ", RED, WHITE)
    
    def draw_game(self):
        """Oyun ekranını çiz"""
        self.screen.fill(DARK_GREEN)
        
        # Başlık ve istatistikler
        title = self.font_medium.render("*** GERCEKCI CASINO BLACKJACK ***", True, GOLD)
        self.screen.blit(title, (30, 30))
        
        stats_text = f"Kar/Zarar: {self.total_profit:+d} | Oyun: {self.games_played} | Kazanilan: {self.games_won} | Kaybedilen: {self.games_lost}"
        stats = self.font_small.render(stats_text, True, WHITE)
        self.screen.blit(stats, (30, 80))
        
        if self.blackjacks_hit > 0:
            bj_text = f"*** Blackjack: {self.blackjacks_hit} ***"
            bj = self.font_small.render(bj_text, True, GOLD)
            self.screen.blit(bj, (30, 110))
        
        # Kasa eli - yukarıda
        dealer_label = self.font_medium.render(">>> KASA:", True, WHITE)
        self.screen.blit(dealer_label, (80, 160))
        
        self.draw_hand(self.dealer_hand, 80, 200, self.hide_dealer_card)
        
        if not self.hide_dealer_card:
            dealer_value = self.font_medium.render(f"Toplam: {self.dealer_hand.get_value()}", True, WHITE)
            self.screen.blit(dealer_value, (80, 360))
        else:
            visible_value = sum(card.get_value() for card in self.dealer_hand.cards[1:]) if len(self.dealer_hand.cards) > 1 else 0
            dealer_value = self.font_medium.render(f"Görünen: {visible_value}", True, WHITE)
            self.screen.blit(dealer_value, (80, 360))
        
        # Oyuncu eli - ortada
        player_label = self.font_medium.render(">>> SEN:", True, WHITE)
        self.screen.blit(player_label, (80, 420))
        
        self.draw_hand(self.player_hand, 80, 460)
        
        player_value = self.font_medium.render(f"Toplam: {self.player_hand.get_value()}", True, WHITE)
        self.screen.blit(player_value, (80, 620))
        
        # Özel durumlar - merkeze
        if self.player_hand.is_blackjack():
            bj_text = self.font_large.render("*** BLACKJACK! ***", True, GOLD)
            bj_rect = bj_text.get_rect(center=(SCREEN_WIDTH//2, 380))
            # Arka plan
            bg_rect = bj_rect.inflate(60, 30)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, GOLD, bg_rect, 4)
            self.screen.blit(bj_text, bj_rect)
        elif self.player_hand.is_bust():
            bust_text = self.font_large.render("XXX PATLADIN! XXX", True, RED)
            bust_rect = bust_text.get_rect(center=(SCREEN_WIDTH//2, 380))
            # Arka plan
            bg_rect = bust_rect.inflate(60, 30)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, RED, bg_rect, 4)
            self.screen.blit(bust_text, bust_rect)
        
        # Mesajlar
        if self.message:
            msg_text = self.font_medium.render(self.message, True, WHITE)
            msg_rect = msg_text.get_rect(center=(SCREEN_WIDTH//2, 680))
            self.screen.blit(msg_text, msg_rect)
        
        # Sonuç mesajı - merkeze büyük
        if self.result_message:
            result_text = self.font_large.render(self.result_message, True, GOLD)
            result_rect = result_text.get_rect(center=(SCREEN_WIDTH//2, 320))
            
            # Arka plan
            bg_rect = result_rect.inflate(80, 40)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, GOLD, bg_rect, 5)
            
            self.screen.blit(result_text, result_rect)
        
        # Butonlar - alt merkez
        can_play = not self.player_hand.is_bust() and not self.player_hand.is_blackjack() and self.game_state == "playing"
        
        self.draw_button(self.buttons["hit"], "KART ÇEK", GREEN if can_play else GRAY, WHITE, can_play)
        self.draw_button(self.buttons["stand"], "DUR", BLUE if can_play else GRAY, WHITE, can_play)
        self.draw_button(self.buttons["new_game"], "YENİ OYUN", GOLD, BLACK)
        self.draw_button(self.buttons["exit"], "ÇIKIŞ", RED, WHITE)
    
    def deal_initial_cards(self):
        """İlk kartları dağıt"""
        self.player_hand.clear()
        self.dealer_hand.clear()
        
        # Oyuncuya 2 kart
        self.player_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        
        # Kasaya 2 kart
        self.dealer_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        
        self.hide_dealer_card = True
        self.message = ""
        self.result_message = ""
    
    def dealer_play(self):
        """Kasa oynar"""
        self.hide_dealer_card = False
        
        while True:
            dealer_value = self.dealer_hand.get_value()
            
            if dealer_value < 17:
                self.dealer_hand.add_card(self.deck.deal_card())
            elif dealer_value == 17 and self.dealer_hand.is_soft():
                # Soft 17'de kart çek (casino avantajı)
                self.dealer_hand.add_card(self.deck.deal_card())
            else:
                break
            
            if self.dealer_hand.is_bust():
                break
    
    def determine_winner(self) -> Tuple[str, int]:
        """Kazananı belirle"""
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        # Oyuncu patladı
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
        if winner == "player":
            if self.player_hand.is_blackjack():
                self.result_message = f"*** BLACKJACK! +{profit} birim ***"
            else:
                self.result_message = f"+++ KAZANDIN! +{profit} birim +++"
        elif winner == "dealer":
            if self.player_hand.is_bust():
                self.result_message = f"XXX PATLADIN! {profit} birim XXX"
            elif self.dealer_hand.is_blackjack():
                self.result_message = f">>> Kasa Blackjack! {profit} birim <<<"
            else:
                self.result_message = f">>> Kasa Kazandi! {profit} birim <<<"
        else:
            self.result_message = "=== BERABERE! ==="
        
        self.total_profit += profit
        
        # İstatistikleri güncelle
        if winner == "player":
            self.games_won += 1
        elif winner == "dealer":
            self.games_lost += 1
        else:
            self.games_tied += 1
    
    def new_game(self):
        """Yeni oyun başlat"""
        self.games_played += 1
        self.deal_initial_cards()
        self.game_state = "playing"
        
        # Blackjack kontrolü
        if self.player_hand.is_blackjack() or self.dealer_hand.is_blackjack():
            self.hide_dealer_card = False
            winner, profit = self.determine_winner()
            self.show_result(winner, profit)
            self.game_state = "result"
    
    def handle_click(self, pos):
        """Tıklama olaylarını işle"""
        if self.game_state == "menu":
            if self.buttons["start"].collidepoint(pos):
                self.new_game()
            elif self.buttons["quit"].collidepoint(pos):
                return False
        
        elif self.game_state in ["playing", "result"]:
            if self.buttons["hit"].collidepoint(pos) and self.game_state == "playing":
                if not self.player_hand.is_bust() and not self.player_hand.is_blackjack():
                    self.player_hand.add_card(self.deck.deal_card())
                    
                    if self.player_hand.is_bust():
                        winner, profit = self.determine_winner()
                        self.show_result(winner, profit)
                        self.game_state = "result"
            
            elif self.buttons["stand"].collidepoint(pos) and self.game_state == "playing":
                if not self.player_hand.is_bust():
                    self.dealer_play()
                    winner, profit = self.determine_winner()
                    self.show_result(winner, profit)
                    self.game_state = "result"
            
            elif self.buttons["new_game"].collidepoint(pos):
                self.new_game()
            
            elif self.buttons["exit"].collidepoint(pos):
                self.game_state = "menu"
        
        return True
    
    def run(self):
        """Ana oyun döngüsü"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Sol tık
                        running = self.handle_click(event.pos)
            
            # Ekranı çiz
            if self.game_state == "menu":
                self.draw_menu()
            else:
                self.draw_game()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = BlackjackGUI()
    game.run() 