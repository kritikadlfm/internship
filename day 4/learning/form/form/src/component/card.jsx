import CardTitle from "./CardTitle"
import CardInfo from "./CardInfo"

function Card(props) {

  return (

    <div className="card">

      <CardTitle
        name={props.name}
      />

      <CardInfo
        role={props.role}
        age={props.age}
        city={props.city}
      />

    </div>

  )

}

export default Card