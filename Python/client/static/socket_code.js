(() => {
    const private_key = "743677397A244326462948404D635166546A576E5A7234753778214125442A47" //in Hex
    class myWebsocketHandler {
        setupSocket() {
            this.socket = new WebSocket("ws://localhost:4000/ws/chat")

            this.socket.addEventListener("message", (event) => {
                const pTag = document.createElement("p")
                pTag.innerHTML = event.data

                document.getElementById("main").append(pTag)
            })

            this.socket.addEventListener("close", () => {
                this.setupSocket()
            })
        }

        submit(event) {
            event.preventDefault()
            const input = document.getElementById("message")
            const message = input.value
            input.value = ""

            this.socket.send(
                JSON.stringify({
                    data: { message: message },
                })
            )
        }
    }

    const ws = new myWebsocketHandler()
    ws.setupSocket()

    document.getElementById("button")
        .addEventListener("click", (event) => ws.submit(event))
})()