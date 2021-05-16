from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
from modules.databaze import Db, Game, Platform


class PlatformContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


class PlatformDialog(MDDialog):
    def __init__(self, *args, **kwargs):
        super(PlatformDialog, self).__init__(
            type="custom",
            content_cls=PlatformContent(),
            title='Nová platforma',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )

    def save_dialog(self, *args):
        platform = Platform()
        platform.name = self.content_cls.ids.platform_name.text
        app.games.database.create_platform(platform)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class GameContent(BoxLayout):
    def __init__(self, id, *args, **kwargs):
        super().__init__(**kwargs)
        if id:
            game = vars(app.games.database.read_by_id(id))
        else:
            game = {"id":"", "name":"", "platform1": "Platforma"}

        self.ids.game_name.text = game['name']
        platforms = app.games.database.read_platforms()
        menu_items = [{"viewclass": "OneLineListItem", "text": f"{platform.name}", "on_release": lambda x=f"{platform.name}": self.set_item(x)} for platform in platforms]
        self.menu_platforms = MDDropdownMenu(
            caller=self.ids.platform_item,
            items=menu_items,
            position="center",
            width_mult=5,
        )
        self.ids.platform_item.set_item(game['platform1'])
        self.ids.platform_item.text = game['platform1']

    def set_item(self, text_item):
        self.ids.platform_item.set_item(text_item)
        self.ids.platform_item.text = text_item
        self.menu_platforms.dismiss()


class GameDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        super(GameDialog, self).__init__(
            type="custom",
            content_cls=GameContent(id=id),
            title='Záznam her',
            text='Ahoj',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )
        self.id = id

    def save_dialog(self, *args):
        game = {}
        game['name'] = self.content_cls.ids.game_name.text
        game['platform1'] = self.content_cls.ids.platform_item.text
        if self.id:
            game["id"] = self.id
            app.games.update(game)
        else:
            app.games.create(game)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class MyItem(TwoLineAvatarIconListItem):
    def __init__(self, item, *args, **kwargs):
        super(MyItem, self).__init__()
        self.id = item['id']
        self.text = item['name']
        self.secondary_text = item['platform1']
        self._no_ripple_effect = True
        self.icon = IconRightWidget(icon="delete", on_release=self.on_delete)
        self.add_widget(self.icon)

    def on_press(self):
        self.dialog = GameDialog(id=self.id)
        self.dialog.open()

    def on_delete(self, *args):
        yes_button = MDFlatButton(text='Ano', on_release=self.yes_button_release)
        no_button = MDFlatButton(text='Ne', on_release=self.no_button_release)
        self.dialog_confirm = MDDialog(type="confirmation", title='Smazání záznamu', text="Chcete opravdu smazat tento záznam?", buttons=[yes_button, no_button])
        self.dialog_confirm.open()

    def yes_button_release(self, *args):
        app.games.delete(self.id)
        self.dialog_confirm.dismiss()

    def no_button_release(self, *args):
        self.dialog_confirm.dismiss()


class Games(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Games, self).__init__(orientation="vertical")
        global app
        app = App.get_running_app()
        scrollview = ScrollView()
        self.list = MDList()
        self.database = Db(dbtype='sqlite', dbname='games.db')
        self.rewrite_list()
        scrollview.add_widget(self.list)
        self.add_widget(scrollview)
        button_box = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        new_game_btn = MDFillRoundFlatIconButton()
        new_game_btn.text = "Nová hra"
        new_game_btn.icon = "plus"
        new_game_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_game_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_game_btn.md_bg_color = [0, 0.5, 0.8, 1]
        new_game_btn.font_style = "Button"
        new_game_btn.pos_hint = {"center_x": .5}
        new_game_btn.on_release = self.on_create_game
        button_box.add_widget(new_game_btn)
        new_platform_btn = MDFillRoundFlatIconButton()
        new_platform_btn.text = "Nová platforma"
        new_platform_btn.icon = "plus"
        new_platform_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_platform_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_platform_btn.md_bg_color = [0.8, 0.5, 0, 1]
        new_platform_btn.font_style = "Button"
        new_platform_btn.pos_hint = {"center_x": .6}
        new_platform_btn.on_release = self.on_create_platform
        button_box.add_widget(new_platform_btn)
        self.add_widget(button_box)


    def rewrite_list(self):
        self.list.clear_widgets()
        games = self.database.read_all()
        for game in games:
            print(vars(game))
            self.list.add_widget(MyItem(item=vars(game)))

    def on_create_game(self, *args):
        self.dialog = GameDialog(id=None)
        self.dialog.open()

    def on_create_platform(self, *args):
        self.dialog = PlatformDialog()
        self.dialog.open()

    def create(self, game):
        create_game = Game()
        create_game.name = game['name']
        create_game.platform1 = game['platform1']
        self.database.create(create_game)
        self.rewrite_list()


    def update(self, game):
        update_game = self.database.read_by_id(game['id'])
        update_game.name = game['name']
        update_game.platform1 = game['platform1']
        self.database.update()
        self.rewrite_list()

    def delete(self, id):
        self.database.delete(id)
        self.rewrite_list()