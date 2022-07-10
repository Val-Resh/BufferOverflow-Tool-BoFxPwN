from Target.target import Target
from Target.target_factory import create_target


class Fuzzer:
    def indentify_crash(self, target: Target, attempts: int = 100):
        size = 100
        for i in range(attempts):
            payload = 'A' * size
            try:
                target.receive_data()
                target.send_data(payload)
                response = target.receive_data()
                if len(response) < 1:
                    return size
                size += 100
            except Exception:
                target.connection.kill()
            if not target.is_alive():
                target = create_target(target.process)
        return 0
