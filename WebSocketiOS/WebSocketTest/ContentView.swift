//
//  ContentView.swift
//  WebSocketTest
//
//  Created by Lily.
//


import SwiftUI
import Foundation
import Combine

class MyObservable: ObservableObject {
    @Published var all_messages = [String]()
}

struct ContentView: View {
    @State var message :String = ""
    @State var all_messages =  [String]()
    @ObservedObject var model:MyObservable = MyObservable()
    
    let urlSession = URLSession(configuration: .default)
    let url = URL(string: "ws://localhost:4000/ws/chat")
    var task:URLSessionWebSocketTask;
    init() {
        task = urlSession.webSocketTask(with: url!)
        task.receive(completionHandler: webSocketCallback)
        task.resume()
    }
    
    var body: some View {
        VStack {
            List {
                ForEach(model.all_messages,id:\.self) {
                    msg in Text(msg)
                }
            }
            
            TextField("Type a message", text: $message)
            Button(action: sendMessage) {
                Text("Send")
            }
        }
    }
    func sendMessage() {
        let ws_message = URLSessionWebSocketTask.Message.string("{\"data\": {\"message\":\"\(message)\"} }")
        //        task.resume()
        task.send(ws_message) {
            error in
            if let error = error {
                print("WebSocket coudn't send message because: \(error)")
            }
        }
        task.resume()
        model.all_messages.append(message)
        message=""
    }
    
    func webSocketCallback(result: Result<URLSessionWebSocketTask.Message, Error>) {
        switch result {
        case .failure(let error):
            print("Error in receiving message: \(error)")
        case .success(let message):
            switch message {
            case .string(let text):
                model.all_messages.append(text)
                print("Received string: \(text)")
            case .data(let data):
                print("Received data: \(data)")
            @unknown default:
                print("Got Here :(")
            }
        }
        task.receive(completionHandler: webSocketCallback)
    }
}
