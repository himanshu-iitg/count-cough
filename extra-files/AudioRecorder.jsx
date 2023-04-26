import { useState, useRef, useEffect } from "react";
// import Recorder from "../src/recorder";

const mimeType = "audio/wav";

const AudioRecorder = () => {
	const [permission, setPermission] = useState(false);

	const mediaRecorder = useRef(null);

	const [audioBlob, setAudioBlob] = useState()

	const [recordingStatus, setRecordingStatus] = useState("inactive");

	const [stream, setStream] = useState(null);

	const [audio, setAudio] = useState(null);

	const [audioChunks, setAudioChunks] = useState([]);

	const getMicrophonePermission = async () => {
		if ("MediaRecorder" in window) {
			try {
				const mediaStream = await navigator.mediaDevices.getUserMedia({
					audio: true,
					video: false,
				});

				// audioContext = new AudioContext();

				// input = audioContext.createMediaStreamSource(mediaStream);

				// rec = new Recorder(input,{numChannels:1})

				// rec.record();

				setPermission(true);
				setStream(mediaStream);
			} catch (err) {
				alert(err.message);
			}
		} else {
			alert("The MediaRecorder API is not supported in your browser.");
		}
	};

	useEffect(() => {
		console.log("audioblob changed", audioBlob)
		// const recordedFile = new File([audioBlob], `test.wav`);
		//   initializes an empty FormData
		// let data = new FormData();
		//   appends the recorded file and language value
		// data.append("file", recordedFile);


		if (audioBlob != undefined) {
			console.log("audioBlob in useeffect", audioBlob);
			const audiotext = audioBlob.text();
			audiotext.then((a) => {
				let formData = new FormData();
      			formData.append('audio', audioBlob);

			const payload = {
				method: 'POST',

				// headers: {
				// 	'Access-Control-Allow-Origin': '*',
				// 	'Access-Control-Allow-Headers': '*',
				// 	// 'Accept': 'text/plain',
				// 	'Accept': 'application/json',
				// 	// 'Content-Type': 'text/plain'
				// 	// 'Content-Type': 'application/json'
				// 	'Content-Type': 'multipart/form-data'
				// },
				body: formData
				// data
				// audioBlob.arrayBuffer()
				// audioBlob.text()
			}
			console.log("fetching request", formData)

      console.log('blob', audioBlob);

    //   $.ajax({
    //     type: 'POST',
    //     url: 'http://127.0.0.1:5000/',
    //     data: formData,
    //     contentType: false,
    //     processData: false,
    //     success: function(result) {
    //       console.log('success', result);
    //     },
    //     error: function(result) {
    //       alert('sorry an error occured');
    //     }
    //   });

			fetch('http://127.0.0.1:5000/', payload)
				.then(response => console.log(response.json()))
				// .then(data => console.log(data))
				.catch(error => console.log("error is", error))
		})}
	}, [audioBlob])

	const startRecording = async () => {
		setRecordingStatus("recording");
		const media = new MediaRecorder(stream, { type: mimeType });

		mediaRecorder.current = media;

		mediaRecorder.current.start();

		let localAudioChunks = [];

		mediaRecorder.current.ondataavailable = (event) => {
			if (typeof event.data === "undefined") return;
			if (event.data.size === 0) return;
			localAudioChunks.push(event.data);
		};

		setAudioChunks(localAudioChunks);
	};

	const stopRecording = () => {
		setRecordingStatus("inactive");
		mediaRecorder.current.stop();

		// rec.stop();

		// rec.exportWAV(createDownloadLink);

		mediaRecorder.current.onstop = () => {
			console.log('blob', audioChunks.blob);
			const audioblob = new Blob(audioChunks, {type:'audio/wav; codecs=MS_PCM'});//new Blob(audioChunks, { type: mimeType });
			const audioUrl = URL.createObjectURL(audioblob);


			console.log('url and blob ', audioUrl, audioblob);

			setAudio(audioUrl);
			setAudioBlob(audioblob)
			// handleData(audioBlob)

		};
	};

	return (
		<div>
			<h2>Audio Recorder</h2>
			<main>
				<div className="audio-controls">
					{!permission ? (
						<button onClick={getMicrophonePermission} type="button">
							Get Microphone
						</button>
					) : null}
					{permission && recordingStatus === "inactive" ? (
						<button onClick={startRecording} type="button">
							Start Recording
						</button>
					) : null}
					{recordingStatus === "recording" ? (
						<button onClick={stopRecording} type="button">
							Stop Recording
						</button>
					) : null}
				</div>
				{audio ? (
					<div className="audio-player">
						<audio src={audio} controls></audio>
						<a download href={audio}>
							Download Recording
						</a>
					</div>
				) : null}
			</main>
		</div>
	);
};

export default AudioRecorder;
