import { useState } from 'react'
import './App.css'
import Vapi from "@vapi-ai/web";

const vapi = new Vapi("12ac47cb-5bb9-423b-9764-07d64d91b8f5");

function App() {
  const [isCallActive, setIsCallActive] = useState(false)

  const startCall = async () => {
    await vapi.start("fbe15d30-b6e9-4192-807e-45edd40c49f0")
    setIsCallActive(true)
  }

  const stopCall = async () => {
    vapi.stop()
    setIsCallActive(false)
  }

  return (
    <div className="container">
      <img 
        src="https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg" 
        alt="Amazon Logo" 
        className="logo" 
      />
      <h1>Amazon Order Status Lookup</h1>
      <p>Voice AI Agent</p>
      <div className={`ripple ${!isCallActive ? 'ripple-static' : ''}`}>
        <div className="ripple-circle"></div>
      </div>
      <div className="button-container">
        <button 
          onClick={startCall} 
          disabled={isCallActive}
          className="call-button"
        >
          Start Call
        </button>
        <button 
          onClick={stopCall} 
          disabled={!isCallActive}
          className="call-button"
        >
          Stop Call
        </button>
      </div>
      <p className="status-text">
        {isCallActive ? 'Call in progress...' : 'Call ended'}
      </p>
    </div>
  )
}

export default App
