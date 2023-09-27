document.addEventListener('DOMContentLoaded', () => {
	const form = document.querySelector('#form')
	socket = null

	socket = new WebSocket('ws://localhost:8000/listen')
	
	socket.onopen = () => {
		console.log({ event: 'onopen' })
	}

	socket.onmessage = (message) => {
		const received = message.data
		if (received) {
			console.log(received)
		}
	}

	socket.onclose = () => {
		console.log({ event: 'onclose' })
	}

	socket.onerror = (error) => {
		console.log({ event: 'onerror', error })
	}
	
	/* const handleData = async (event) => {
		if (event.data.size > 0 && socket.readyState == 1) {
			socket.send(event.data)
		}
	} */

	form.addEventListener('submit', (event) => {
		event.preventDefault()
		const data = new FormData(form)
		const prediction = data.get('prediction')
		if (prediction) {
			socket.send(prediction)
			form.reset()
		}
	})
})