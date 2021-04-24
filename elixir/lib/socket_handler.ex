defmodule Ilopotion.SocketHandler do
    @behaviour :cowboy_websocket

    def init(request, _state) do
      state = %{registry_key: request.path}
			r = HTTPoison.post!('http://0.0.0.0:8000/potion', {:multipart, [
          {"address", elem(request.peer,0) |> Tuple.to_list |> Enum.join(".")}
			]})
			try do
				if r.body == "false" do
					Process.exit(self(),:kill)
				end
      catch
					:throw,_ -> raise "Potion Failed to reply"
			end
      {:cowboy_websocket, request, state}
    end

    def websocket_init(state) do
      Registry.Ilopotion
      |> Registry.register(state.registry_key, {})

      {:ok, state}
    end

    def websocket_handle({:text, json}, state) do
      payload = Jason.decode!(json)
      message = payload["data"]["message"]

      Registry.Ilopotion
      |> Registry.dispatch( state.registry_key, fn(entries) ->
          for {pid, _} <- entries do
            if pid != self() do
              Process.send(pid, message, [])
            end
          end
        end
      )

      {:reply, {:text, message}, state}
    end

    def websocket_info(info, state) do
      {:reply, {:text, info}, state}
    end
  end