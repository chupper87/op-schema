import { useState } from 'react'
import './App.css'

function App() {

  const [isLoggedIn, setIsLoggedIn] = useState(false)


  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-blue-400">
        <div className="login-container">

          <h2>Login</h2><div />
          <input type="text" placeholder="Username" className="login-input" /><div />
          <input type="password" placeholder="Password" className="login-input" /><div />
          <button className="login-button" onClick={() => setIsLoggedIn(true)}>Login</button>
        </div>
      </div>
    )

  } else {
    return (
      <div>
        <h1 className=''>Hello!</h1>
      </div>
    )
  }


}

export default App