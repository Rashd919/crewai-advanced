class Application:
    def __init__(self):
        self.title = "مركز العمليات الاستخباراتية"

    def run(self):
        print(f"running application: {self.title}")

if __name__ == "__main__":
    app = Application()
    app.run()
