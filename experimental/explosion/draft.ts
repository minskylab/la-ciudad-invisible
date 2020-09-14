let board = [];
let cellSize = 5;

function setup() {
    createCanvas(500, 500);
    for (let i = 0; i < width / cellSize; i++) {
        let row = [];
        for (let j = 0; j < height / cellSize; j++) {
            // row.push(noise(i*width/cellSize + j) > 0.5);
            row.push(false);
        }
        board.push(row);
    }

    noStroke();
    // noLoop();
}

function draw() {
    background(220);
    for (let i = 0; i < width / cellSize; i++) {
        for (let j = 0; j < height / cellSize; j++) {
            if (board[i][j]) {
                fill(255);
            } else {
                fill(0);
            }

            // stroke("red");
            rect(i * cellSize, j * cellSize, (i + 1) * cellSize, (j + 1) * cellSize);

            // fill("green")
            // stroke("green");
            // text(`(${i}, ${j})`,i*cellSize+10, j*cellSize+20)
        }
    }

    let nextBoard = [...board.map((r) => [...r])];
    for (let i = 0; i < width / cellSize; i++) {
        for (let j = 0; j < height / cellSize; j++) {
            let n = 0;

            for (let y = -1; y <= 1; y++) {
                for (let x = -1; x <= 1; x++) {
                    if (x === 0 && y === 0) continue;

                    const nx = i + x;
                    const ny = j + y;

                    const x_out_bound = nx < 0 || nx >= board.length;
                    const y_out_bound = ny < 0 || ny >= board[0].length;

                    if (x_out_bound || y_out_bound) {
                        continue;
                    }

                    if (board[nx][ny] === true) {
                        n += 1;
                    }

                    // console.log(`(${i}, ${j})<${x},${y}>[${nx}, ${ny}] = ${board[nx][ny]}`)
                    // if (board[nx] !== undefined) {
                    // if (board[nx][ny] !== undefined) {
                    // n += board[nx][ny]? 1: 0;
                    // }
                    // }
                }
            }

            // fill("blue")
            // stroke("blue");
            // text(`${n}`,i*cellSize+10, j*cellSize+40)
            const ns = n === 3 || (board[i][j] && n === 2);
            nextBoard[i][j] = ns;
        }
    }

    board = [...nextBoard];
}

function draw_noisy_circle(x, y, r) {
    for (let i = 0; i < width / cellSize; i++) {
        for (let j = 0; j < height / cellSize; j++) {
            const near = r + noise(millis()) * 5 + random() * 2;

            board[i][j] = dist(i, j, x, y) < near ? (random() < 0.5 ? true : board[i][j]) : board[i][j];
        }
    }
}

function mousePressed() {
    draw_noisy_circle(mouseX / cellSize, mouseY / cellSize, 5);
}
