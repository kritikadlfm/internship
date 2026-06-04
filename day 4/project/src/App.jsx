import react from "react";
import axios from 'axios';
const App = () => {
  const [data, setData] = useState([]);
  const getData = async() => {
    const response = await axios.get('https://picsum.photos/v2/list?page=2&limit=100')
    setData(response.data);
    console.log(data)
  }
  getData()
  return (
    <div className='p-10'>
      <button className='bg-teal-700 text-white font-semibold text-2xl px-6 py-3 rounded-lg hover:bg-teal-500 transition duration-300'>
        Get Data 
      </button>
      <div className='p-5 bg-gray-100 mt-5 rounded-lg'>
        <p className='text-gray-700 text-lg'>Data will be displayed here...</p>
      </div>
    </div>
   )
}
export default App