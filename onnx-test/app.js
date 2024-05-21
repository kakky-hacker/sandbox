const canvas = document.getElementById('input-canvas');
const ctx = canvas.getContext('2d');
let painting = false;

function startPosition(e) {
    painting = true;
    draw(e);
}

function endPosition() {
    painting = false;
    ctx.beginPath();
}

function draw(e) {
    if (!painting) return;
    ctx.lineWidth = 15;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';

    ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function getImageTensor() {
    const ctx = document.getElementById('input-canvas').getContext('2d');
    const ctxScaled = document.getElementById('input-canvas-scaled').getContext('2d');
    ctxScaled.save();
    ctxScaled.scale(28 / ctx.canvas.width, 28 / ctx.canvas.height);
    ctxScaled.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctxScaled.drawImage(document.getElementById('input-canvas'), 0, 0);
    ctxScaled.restore();

    const imageDataScaled = ctxScaled.getImageData(0, 0, 28, 28);
    const input = new Float32Array(784);
    for (let i = 0, len = imageDataScaled.data.length; i < len; i += 4) {
        input[i / 4] = imageDataScaled.data[i + 3] / 255;
    }
    const tensor = new onnx.Tensor(input, 'float32', [1, 1, 28, 28]);

    return tensor;
}

async function predict() {
    console.log("Prediction started");

    const inputTensor = getImageTensor();
    console.log("Input tensor created");

    const session = new onnx.InferenceSession({ backendHint: 'cpu' });
    const modelFile = './mnist.onnx';

    try {
        await session.loadModel(modelFile);
        console.log("Model loaded successfully");

        const outputData = await session.run([inputTensor]);
        console.log("Output data:", outputData);

        if (outputData) {
            const outputTensor = outputData.values().next().value;
            console.log("Output tensor:", outputTensor);

            const prediction = outputTensor.data.indexOf(Math.max(...outputTensor.data));
            document.getElementById('prediction').innerText = `Prediction: ${prediction}`;
            console.log(`Prediction: ${prediction}`);
        } else {
            console.error("No output data received from the model.");
        }
    } catch (err) {
        console.error("Error during prediction:", err);
        alert("An error occurred during prediction. Please check the console for more details.");
    }
}

canvas.addEventListener('mousedown', startPosition);
canvas.addEventListener('mouseup', endPosition);
canvas.addEventListener('mousemove', draw);
