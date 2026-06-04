import { useState } from "react"

function App() {

  const [count, setCount] = useState(0)

  function increaseCount() {
    setCount(count + 1)
  }

  function decreaseCount() {

    if (count > 0) {
      setCount(count - 1)
    }

  }

  function resetCount() {
    setCount(0)
  }

  return (

    <div>

      <h1>Count: {count}</h1>

      <button onClick={increaseCount}>
        Increase
      </button>

      <button onClick={decreaseCount}>
        Decrease
      </button>

      <button onClick={resetCount}>
        Reset
      </button>

    </div>

  )

}

export default App