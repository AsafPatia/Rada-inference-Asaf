from pydantic import BaseSettings


class Settings(BaseSettings):
    # TODO change client_port to his real default 7034
    log_level = "DEBUG"

    host_ip = '127.0.0.1'
    host_port = 7033
    client_ip = '127.0.0.1'
    client_port = 7033
    # client_port = 7034
    unknown_prediction_code = 1
    drone_prediction_code = 8
    not_drone_prediction_code = 9
    plot_sliding_window_size = 10
    idle_track_purging_frequency = 10


settings = Settings()
