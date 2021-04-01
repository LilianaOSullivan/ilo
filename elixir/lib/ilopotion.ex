defmodule Ilopotion do
  use Application

  def start(_type, _args) do
    HTTPoison.start
    children = [
      Plug.Cowboy.child_spec(
        scheme: :http,
        plug: Ilopotion.Router,
        options: [
          dispatch: dispatch(),
          port: 4000
        ]
      ),
      Registry.child_spec(
        keys: :duplicate,
        name: Registry.Ilopotion
      )
    ]

    opts = [strategy: :one_for_one, name: Ilopotion.Application]
    Supervisor.start_link(children, opts)
  end

  defp dispatch do
    [
      {:_,
        [
          {"/ws/[...]", Ilopotion.SocketHandler, []},
          {:_, Plug.Cowboy.Handler, {Ilopotion.Router, []}}
        ]
      }
    ]
  end
end