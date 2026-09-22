from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
import sqlite3
import random
from datetime import datetime
from pathlib import Path


APP_NAME = "ACTION & VÉRITÉ"

KV = r"""
#:import dp kivy.metrics.dp

<Header@BoxLayout>:
    size_hint_y: None
    height: dp(70)
    padding: dp(12)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: .08, .09, .13, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [0, 0, 12, 12]
    Label:
        text: root.title if hasattr(root, "title") else "ACTION & VÉRITÉ"
        font_size: "22sp"
        bold: True
        color: 1, 1, 1, 1

<NavButton@Button>:
    size_hint_y: None
    height: dp(52)
    font_size: "16sp"
    background_normal: ""
    background_color: .20, .12, .45, 1
    color: 1, 1, 1, 1

<MainButton@Button>:
    size_hint_y: None
    height: dp(52)
    font_size: "16sp"
    background_normal: ""
    background_color: .49, .23, .82, 1
    color: 1, 1, 1, 1

<SecondaryButton@Button>:
    size_hint_y: None
    height: dp(48)
    font_size: "15sp"
    background_normal: ""
    background_color: .13, .15, .20, 1
    color: 1, 1, 1, 1

<GameScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(10)

        BoxLayout:
            size_hint_y: None
            height: dp(48)
            Label:
                text: "🎲  ACTION & VÉRITÉ"
                font_size: "23sp"
                bold: True
                color: .95, .95, 1, 1
            Label:
                text: root.round_text
                font_size: "14sp"
                color: .60, .65, .72, 1
                size_hint_x: .35

        BoxLayout:
            size_hint_y: None
            height: dp(55)
            spacing: dp(8)
            Spinner:
                id: player_spinner
                text: "Choisir un joueur"
                values: root.player_names
                font_size: "16sp"
            Spinner:
                id: kind_spinner
                text: "Aléatoire"
                values: ["Aléatoire", "Vérité", "Action"]
                font_size: "16sp"

        BoxLayout:
            orientation: "vertical"
            padding: dp(18)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: .09, .10, .14, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [18, 18, 18, 18]

            Label:
                text: root.kind_text
                font_size: "20sp"
                bold: True
                color: .93, .30, .65, 1
                size_hint_y: None
                height: dp(45)

            Label:
                text: root.challenge_text
                font_size: "24sp"
                bold: True
                halign: "center"
                valign: "middle"
                text_size: self.width, None

            Label:
                text: root.timer_text
                font_size: "30sp"
                bold: True
                color: .96, .62, .05, 1
                size_hint_y: None
                height: dp(55)

            Label:
                text: root.status_text
                font_size: "15sp"
                color: .60, .65, .72, 1
                halign: "center"
                text_size: self.width, None
                size_hint_y: None
                height: dp(50)

            BoxLayout:
                size_hint_y: None
                height: dp(52)
                spacing: dp(8)
                MainButton:
                    text: "🎲 Nouvelle"
                    on_release: root.new_round()
                SecondaryButton:
                    text: "⏱ 30 s"
                    on_release: root.start_timer(30)

            BoxLayout:
                size_hint_y: None
                height: dp(52)
                spacing: dp(8)
                Button:
                    text: "✓ Réussi +10"
                    background_normal: ""
                    background_color: .13, .70, .32, 1
                    font_size: "15sp"
                    on_release: root.finish_round(True)
                Button:
                    text: "✕ Refusé"
                    background_normal: ""
                    background_color: .85, .16, .18, 1
                    font_size: "15sp"
                    on_release: root.finish_round(False)

        BoxLayout:
            size_hint_y: None
            height: dp(55)
            spacing: dp(8)
            NavButton:
                text: "👥 Joueurs"
                on_release: app.go("players")
            NavButton:
                text: "🏆 Scores"
                on_release: app.go("scores")
            NavButton:
                text: "📝 Questions"
                on_release: app.go("questions")
            NavButton:
                text: "📜 Historique"
                on_release: app.go("history")

<PlayersScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(10)
        Label:
            text: "👥  JOUEURS"
            size_hint_y: None
            height: dp(48)
            font_size: "24sp"
            bold: True
        BoxLayout:
            size_hint_y: None
            height: dp(52)
            spacing: dp(8)
            TextInput:
                id: name_input
                hint_text: "Nom du joueur..."
                multiline: False
                font_size: "16sp"
            MainButton:
                text: "＋ Ajouter"
                size_hint_x: .35
                on_release: root.add_player()
        ScrollView:
            GridLayout:
                id: player_list
                cols: 1
                spacing: dp(8)
                padding: dp(5)
                size_hint_y: None
                height: self.minimum_height
        SecondaryButton:
            text: "← Retour au jeu"
            on_release: app.go("game")

<ScoresScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(10)
        Label:
            text: "🏆  CLASSEMENT"
            size_hint_y: None
            height: dp(48)
            font_size: "24sp"
            bold: True
        ScrollView:
            GridLayout:
                id: score_list
                cols: 1
                spacing: dp(8)
                padding: dp(5)
                size_hint_y: None
                height: self.minimum_height
        BoxLayout:
            size_hint_y: None
            height: dp(52)
            spacing: dp(8)
            SecondaryButton:
                text: "↻ Actualiser"
                on_release: root.refresh()
            Button:
                text: "Réinitialiser"
                background_normal: ""
                background_color: .85, .16, .18, 1
                on_release: root.reset_scores()
            SecondaryButton:
                text: "← Retour"
                on_release: app.go("game")

<QuestionsScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(10)
        Label:
            text: "📝  QUESTIONS PERSONNALISÉES"
            size_hint_y: None
            height: dp(60)
            font_size: "21sp"
            bold: True
        Spinner:
            id: q_kind
            text: "Vérité"
            values: ["Vérité", "Action"]
            size_hint_y: None
            height: dp(52)
        TextInput:
            id: q_input
            hint_text: "Écris une nouvelle vérité ou action..."
            multiline: True
            font_size: "16sp"
        MainButton:
            text: "＋ Ajouter"
            on_release: root.add_question()
        Label:
            id: info
            text: ""
            color: .30, .80, .45, 1
            size_hint_y: None
            height: dp(40)
        SecondaryButton:
            text: "← Retour au jeu"
            on_release: app.go("game")

<HistoryScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(10)
        Label:
            text: "📜  HISTORIQUE"
            size_hint_y: None
            height: dp(48)
            font_size: "24sp"
            bold: True
        ScrollView:
            Label:
                id: history_label
                text: "Aucun historique."
                font_size: "14sp"
                text_size: self.width, None
                halign: "left"
                valign: "top"
                size_hint_y: None
                height: self.texture_size[1] + dp(20)
                padding: dp(10), dp(10)
        BoxLayout:
            size_hint_y: None
            height: dp(52)
            spacing: dp(8)
            SecondaryButton:
                text: "↻ Actualiser"
                on_release: root.refresh()
            SecondaryButton:
                text: "← Retour"
                on_release: app.go("game")
"""


DEFAULT_QUESTIONS = {
    "Vérité": [
        "Quel est ton plus gros fou rire de cette année ?",
        "Quelle habitude aimerais-tu changer ?",
        "Quel talent caché as-tu ?",
        "Quelle est la chose la plus courageuse que tu aies faite ?",
        "Quel film ou série pourrais-tu revoir plusieurs fois ?",
        "Quelle est ta plus grande qualité selon toi ?",
        "Quelle petite chose te met immédiatement de bonne humeur ?",
        "Quel métier aurais-tu aimé essayer ?",
        "Quel est ton souvenir d'enfance préféré ?",
        "Quelle chanson connais-tu presque par cœur ?",
        "Quelle est une chose que peu de gens savent sur toi ?",
        "Quelle destination aimerais-tu visiter ?",
    ],
    "Action": [
        "Fais 10 secondes de danse sans musique.",
        "Imite un animal choisi par le groupe.",
        "Fais une pose de super-héros pendant 15 secondes.",
        "Chante le refrain d'une chanson choisie par le groupe.",
        "Fais trois compliments sincères à trois joueurs différents.",
        "Parle avec une voix de robot pendant 30 secondes.",
        "Fais semblant de présenter un journal télévisé pendant 20 secondes.",
        "Fais 5 squats si tu peux le faire sans risque.",
        "Invente un slogan pour le joueur à ta gauche.",
        "Mime un métier et laisse les autres deviner.",
        "Fais une mini publicité pour un objet posé devant toi.",
        "Raconte une histoire en utilisant trois mots choisis par le groupe.",
    ],
}


class Database:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                score INTEGER NOT NULL DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                text TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                kind TEXT NOT NULL,
                challenge TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        self.connection.commit()
        self.seed_questions()

    def seed_questions(self):
        total = self.connection.execute(
            "SELECT COUNT(*) AS total FROM questions"
        ).fetchone()["total"]

        if total:
            return

        for kind, questions in DEFAULT_QUESTIONS.items():
            for question in questions:
                self.connection.execute(
                    "INSERT INTO questions (kind, text) VALUES (?, ?)",
                    (kind, question),
                )
        self.connection.commit()

    def add_player(self, name):
        name = name.strip()
        if not name:
            return False, "Le nom est vide."
        try:
            self.connection.execute(
                "INSERT INTO players (name) VALUES (?)",
                (name,),
            )
            self.connection.commit()
            return True, "Joueur ajouté."
        except sqlite3.IntegrityError:
            return False, "Ce joueur existe déjà."

    def delete_player(self, player_id):
        self.connection.execute(
            "DELETE FROM players WHERE id = ?",
            (player_id,),
        )
        self.connection.commit()

    def players(self):
        return self.connection.execute(
            "SELECT * FROM players ORDER BY id"
        ).fetchall()

    def add_score(self, name, points):
        self.connection.execute(
            "UPDATE players SET score = score + ? WHERE name = ?",
            (points, name),
        )
        self.connection.commit()

    def reset_scores(self):
        self.connection.execute("UPDATE players SET score = 0")
        self.connection.commit()

    def random_question(self, kind):
        row = self.connection.execute(
            """
            SELECT text FROM questions
            WHERE kind = ?
            ORDER BY RANDOM()
            LIMIT 1
            """,
            (kind,),
        ).fetchone()
        return row["text"] if row else "Aucun défi disponible."

    def add_question(self, kind, text):
        text = text.strip()
        if not text:
            return False
        self.connection.execute(
            "INSERT INTO questions (kind, text) VALUES (?, ?)",
            (kind, text),
        )
        self.connection.commit()
        return True

    def save_history(self, player, kind, challenge, result):
        self.connection.execute(
            """
            INSERT INTO history
            (player, kind, challenge, result, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                player,
                kind,
                challenge,
                result,
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            ),
        )
        self.connection.commit()

    def history(self):
        return self.connection.execute(
            """
            SELECT player, kind, challenge, result, created_at
            FROM history
            ORDER BY id DESC
            LIMIT 200
            """
        ).fetchall()

    def close(self):
        self.connection.close()


class GameScreen(Screen):
    player_names = StringProperty([])
    round_text = StringProperty("Manche 0")
    kind_text = StringProperty("ACTION & VÉRITÉ")
    challenge_text = StringProperty("Choisis un joueur puis lance une manche.")
    timer_text = StringProperty("")
    status_text = StringProperty("Prêt à jouer.")

    def on_pre_enter(self):
        self.refresh_players()

    def refresh_players(self):
        players = App.get_running_app().db.players()
        self.player_names = [row["name"] for row in players]
        if self.player_names:
            self.ids.player_spinner.text = self.player_names[0]
        else:
            self.ids.player_spinner.text = "Choisir un joueur"

    def popup(self, title, message):
        box = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
        )
        box.add_widget(Label(text=message))
        close = Button(text="OK", size_hint_y=None, height=dp(45))
        box.add_widget(close)
        popup = Popup(
            title=title,
            content=box,
            size_hint=(.88, .40),
        )
        close.bind(on_release=popup.dismiss)
        popup.open()

    def new_round(self):
        player = self.ids.player_spinner.text
        if player == "Choisir un joueur":
            self.popup("Joueurs", "Ajoute d'abord au moins un joueur.")
            return

        selected = self.ids.kind_spinner.text
        kind = random.choice(["Vérité", "Action"]) if selected == "Aléatoire" else selected

        self.kind_text = kind.upper()
        self.challenge_text = App.get_running_app().db.random_question(kind)
        self.status_text = f"{player}, à toi de jouer !"
        self.round_text = f"Manche {App.get_running_app().next_round()}"
        self.timer_text = ""

        App.get_running_app().current_player = player
        App.get_running_app().current_kind = kind
        App.get_running_app().current_challenge = self.challenge_text

    def start_timer(self, seconds):
        if not App.get_running_app().current_challenge:
            self.popup("Chronomètre", "Lance d'abord une manche.")
            return

        app = App.get_running_app()
        app.remaining = seconds
        if app.timer_event:
            app.timer_event.cancel()
        app.timer_event = Clock.schedule_interval(self.tick, 1)

    def tick(self, dt):
        app = App.get_running_app()
        self.timer_text = f"⏱ {app.remaining}s"
        if app.remaining <= 0:
            app.timer_event.cancel()
            app.timer_event = None
            self.status_text = "Temps écoulé ! Décide si le défi est réussi."
            return
        app.remaining -= 1

    def finish_round(self, success):
        app = App.get_running_app()
        if not app.current_challenge or not app.current_player:
            self.popup("Manche", "Lance d'abord une manche.")
            return

        result = "Réussi" if success else "Refusé"
        points = 10 if success else 0

        app.db.add_score(app.current_player, points)
        app.db.save_history(
            app.current_player,
            app.current_kind,
            app.current_challenge,
            result,
        )

        self.status_text = f"{result} — {app.current_player} : +{points} point(s)."
        app.current_challenge = None
        app.refresh_all()


class PlayersScreen(Screen):
    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        layout = self.ids.player_list
        layout.clear_widgets()
        players = App.get_running_app().db.players()

        if not players:
            layout.add_widget(Label(
                text="Aucun joueur.",
                size_hint_y=None,
                height=dp(50),
            ))
            return

        for player in players:
            row = BoxLayout(
                size_hint_y=None,
                height=dp(50),
                spacing=dp(8),
            )
            row.add_widget(Label(
                text=f"{player['name']} — {player['score']} pts",
                halign="left",
            ))
            delete = Button(
                text="Supprimer",
                size_hint_x=.30,
                background_normal="",
                background_color=(.85, .16, .18, 1),
            )
            delete.bind(
                on_release=lambda btn, pid=player["id"]: self.delete(pid)
            )
            row.add_widget(delete)
            layout.add_widget(row)

    def add_player(self):
        name = self.ids.name_input.text
        success, message = App.get_running_app().db.add_player(name)
        if success:
            self.ids.name_input.text = ""
            self.refresh()
            App.get_running_app().refresh_all()
        else:
            self.show_message(message)

    def delete(self, player_id):
        App.get_running_app().db.delete_player(player_id)
        self.refresh()
        App.get_running_app().refresh_all()

    def show_message(self, message):
        box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        box.add_widget(Label(text=message))
        close = Button(text="OK", size_hint_y=None, height=dp(45))
        box.add_widget(close)
        popup = Popup(title="Joueur", content=box, size_hint=(.85, .35))
        close.bind(on_release=popup.dismiss)
        popup.open()


class ScoresScreen(Screen):
    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        layout = self.ids.score_list
        layout.clear_widgets()
        players = sorted(
            App.get_running_app().db.players(),
            key=lambda row: row["score"],
            reverse=True,
        )

        if not players:
            layout.add_widget(Label(
                text="Aucun joueur.",
                size_hint_y=None,
                height=dp(50),
            ))
            return

        medals = ["🥇", "🥈", "🥉"]
        for position, player in enumerate(players, start=1):
            medal = medals[position - 1] if position <= 3 else f"{position}."
            layout.add_widget(Label(
                text=f"{medal}  {player['name']}   —   {player['score']} pts",
                font_size="18sp",
                size_hint_y=None,
                height=dp(55),
            ))

    def reset_scores(self):
        App.get_running_app().db.reset_scores()
        self.refresh()
        App.get_running_app().refresh_all()


class QuestionsScreen(Screen):
    def add_question(self):
        kind = self.ids.q_kind.text
        text = self.ids.q_input.text.strip()

        if not text:
            self.ids.info.text = "Écris une question ou une action."
            return

        if App.get_running_app().db.add_question(kind, text):
            self.ids.q_input.text = ""
            self.ids.info.text = f"{kind} ajoutée avec succès."


class HistoryScreen(Screen):
    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        rows = App.get_running_app().db.history()

        if not rows:
            self.ids.history_label.text = "Aucune manche terminée."
            return

        parts = []
        for row in rows:
            parts.append(
                f"[{row['created_at']}]\n"
                f"{row['player']} — {row['kind']} — {row['result']}\n"
                f"{row['challenge']}\n"
                f"{'-' * 35}\n"
            )

        self.ids.history_label.text = "\n".join(parts)


class ActionVeriteApp(App):
    def build(self):
        self.title = APP_NAME

        data_dir = Path(self.user_data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)

        self.db = Database(str(data_dir / "action_verite.db"))

        self.current_player = None
        self.current_kind = None
        self.current_challenge = None
        self.remaining = 0
        self.timer_event = None
        self.round_number = 0

        Builder.load_string(KV)

        manager = ScreenManager()
        manager.add_widget(GameScreen(name="game"))
        manager.add_widget(PlayersScreen(name="players"))
        manager.add_widget(ScoresScreen(name="scores"))
        manager.add_widget(QuestionsScreen(name="questions"))
        manager.add_widget(HistoryScreen(name="history"))

        return manager

    def go(self, screen_name):
        self.root.current = screen_name

    def next_round(self):
        self.round_number += 1
        return self.round_number

    def refresh_all(self):
        for name in ["game", "players", "scores", "history"]:
            screen = self.root.get_screen(name)
            if hasattr(screen, "refresh"):
                screen.refresh()

        self.root.get_screen("game").refresh_players()

    def on_stop(self):
        if self.timer_event:
            self.timer_event.cancel()
        self.db.close()


if __name__ == "__main__":
    ActionVeriteApp().run()
