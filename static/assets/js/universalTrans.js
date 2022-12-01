// send to server  
const sendAudioFile = file => {

  // get vars from dropdowns
  var sourceLangVal = document.getElementById("sourceLangID").value; // coming from this language
  var destLangVal = document.getElementById("destinationLangID").value; // going to this language
  console.log(sourceLangVal)
  console.log(destLangVal)


  const formData = new FormData();
  formData.append('source-language', sourceLangVal)
  formData.append('destination-language', destLangVal)

  formData.append('audio-file', file);
  return fetch('http://localhost:5000/audioUpload', {
    mode: 'no-cors',
    method: 'POST',
    body: formData
  })
  // .then((responseData) => {console.log(responseData)});
};


// Stop and save data from the microphone
const startButton = document.getElementById('start');
const downloadLink = document.getElementById('download');
const stopButton = document.getElementById('stop');


const handleSuccess = function(stream) {
  const options = {mimeType: 'audio/webm'};
  const recordedChunks = [];  // this is where audio data will be stored -- can be made into a blob
  const mediaRecorder = new MediaRecorder(stream, options);

  // Event starts recording
  startButton.addEventListener('click', function() {
    mediaRecorder.start();
  });

  // Event makes sure that download is not empty
  mediaRecorder.addEventListener('dataavailable', function(e) {
    if (e.data.size > 0) recordedChunks.push(e.data);
  });

  // Event saves + downloads file
  mediaRecorder.addEventListener('stop', function() {
    downloadLink.href = URL.createObjectURL(new Blob(recordedChunks));
    downloadLink.download = 'microphoneAudioWAV.wav';

//   // Create a Blob when recording has stopped.
      const blob = new Blob(recordedChunks, { 
        // 'type': 'audio/mp3' 
        'type': 'audio/wav' 
        });


        var result = sendAudioFile(blob);
        console.log(result)


  });

  // Event stops recording
  stopButton.addEventListener('click', function() {
    mediaRecorder.stop();
  });


};
// only want audio, not webcam
navigator.mediaDevices.getUserMedia({ audio: true, video: false })
    .then(handleSuccess);


// // ----------------------------------

// https://stackoverflow.com/questions/33765865/how-to-swap-two-dropdownlists-with-one-button-using-javascript

const swapButton = document.getElementById('swap');

// Event commences swap
swapButton.addEventListener('click', function() {
  let currentSource = document.getElementById('sourceLangID').value;
  let currentDestination = document.getElementById('destinationLangID').value;

  temp=currentDestination;

  console.log(`Source: ${currentSource}, Destination: ${currentDestination}`)

  currentSource.value = currentDestination.value
  currentSource = currentDestination

  currentDestination.value = temp.value
  currentDestination = temp

  
  console.log("Swapped!")
});