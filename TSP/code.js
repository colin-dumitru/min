var num_cities = 10,
    num_particles = 100,
    main_canvas = null,
    main_context = null,

    fitness_canvas = null,
    fitness_context = null,

    width = null,
    height = null,
    fitness_width = null,
    fitness_height = null,
    width_ratio,

    cities = [],
    particles = [],
    particles_best = [],
    global = null,
    velocities = [];

function randomCity() {
    return {
        x: Math.random() * width,
        y: Math.random() * height
    }
}

function swap(array, index1, index2) {
    var temp = array[index1];
    array[index1] = array[index2];
    array[index2] = temp;
}

function shuffle(array) {
    var currentIndex = array.length,
        randomIndex;

    while (0 != currentIndex) {

        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        swap(array, currentIndex, randomIndex);
    }

    return array;
}

function randomParticle() {
    var order = [];

    for (var i = 0; i < num_cities; i++) {
        order.push(i);
    }
    return shuffle(order);
}

function initialize() {
    for (var i = 0; i < num_cities; i++) {
        cities.push(randomCity());
    }

    for (var i = 0; i < num_particles; i++) {
        velocities.push([]);
        particles.push(randomParticle());
    }
}

function clearMain() {
    main_context.clearRect(0, 0, width, height);
    fitness_context.clearRect(0, 0, width, height);
}

function drawCities() {
    cities.forEach(function(c) {
        main_context.beginPath();
        main_context.arc(c.x, c.y, 10, 0, 2 * Math.PI, false);
        main_context.fill();
    });
}

function drawParticles() {
    particles.forEach(function(p) {
        main_context.beginPath();
        /* For each city in the particle*/
        main_context.moveTo(cities[p[p.length - 1]].x, cities[p[p.length - 1]].y);

        p.forEach(function(c, index) {
            if (index == 0) {
                main_context.lineTo(cities[c].x, cities[c].y);
            } else {
                main_context.lineTo(cities[c].x, cities[c].y);
            }
        });
        main_context.stroke();
    });
}

function drawFitness() {
    var cell_height = fitness_height / num_particles,
        width = 0,
        global_fitness = global && fitness(global);

    particles.forEach(function(p, index) {
        if (!p) {
            return;
        }

        fitness_context.beginPath();
        /* For each city in the particle*/
        width = fitness(p) * width_ratio;

        fitness_context.moveTo(0, cell_height * index);
        fitness_context.lineTo(width, cell_height * index);
        fitness_context.stroke();
    });

    fitness_context.fillRect(global_fitness * width_ratio, 0, 2, fitness_height);
}

function addVel(p, v) {
    p = p.slice(0);

    v.forEach(function(l) {
        swap(p, l.i, l.j);
    });
    return p;
}

function subPos(p1, p2) {
    var vel = [],
        index = 0;

    p1 = p1.slice(0);

    for (var i = 0; i < p1.length - 1; i++) {
        if (p1[i] != p2[i]) {
            index = p1.indexOf(p2[i], i);

            vel.push({
                i: i,
                j: index
            });
            swap(p1, i, index);
        }
    }

    return vel;
}

function combVel(v1, v2) {
    return v1.concat(v2);
}

function mulVel(c, v) {
    var res = [];

    for (var i = 0; i < Math.floor(c); i++) {
        res = res.concat(v);
    }

    for (var i = 0; i < Math.floor((c - Math.floor(c)) * v.length); i++) {
        res.push(v[i]);
    }
    return res;
}

function distance(c1, c2) {
    return Math.sqrt((c2.x - c1.x) * (c2.x - c1.x) + (c2.y - c1.y) * (c2.y - c1.y));
}

function fitness(p) {
    var sum = 0;

    for (var index = 0; index < p.length; index++) {
        if (index == 0) {
            sum += distance(cities[p[p.length - 1]], cities[p[index]]);
        } else {
            sum += distance(cities[p[index - 1]], cities[p[index]]);
        }
    };

    return sum;
}

function updateParticle(x, index) {
    var c1 = 0.5,
        c2 = Math.random() * 2,
        c3 = Math.random() * 2,

        cur_vel = velocities[index],
        p = particles_best[index] || x,
        g = global || x,

        vel_best = mulVel(c2, subPos(p, x)),
        vel_global = mulVel(c3, subPos(g, x)),
        // c1 * v + c2*( p - x ) + c3*(g - x)
        vel = combVel(combVel(mulVel(c1, cur_vel), vel_best), vel_global),
        // x + v
        pos = addVel(x, vel);

    particles[index] = pos;
    // also compress the velocity
    velocities[index] = subPos(pos, x);

    if (!particles_best[index] || (fitness(pos) < fitness(particles_best[index]))) {
        particles_best[index] = pos;
    }

}

function tick() {
    particles.forEach(updateParticle);

    particles_best.forEach(function(p) {
        if (!global || (fitness(p) < fitness(global))) {
            global = p;
        }
    });

    if (!width_ratio) {
        width_ratio = fitness_width / fitness(global) * 0.5;
    }
}

function draw() {
    clearMain();

    drawParticles();
    drawCities();
    drawFitness();

    requestAnimationFrame(draw);
}

$(document).ready(function() {
    main_canvas = $('#main_canvas');
    fitness_canvas = $('#fitness_canvas');

    main_context = main_canvas.get()[0].getContext('2d');
    fitness_context = fitness_canvas.get()[0].getContext('2d');

    width = main_canvas.width();
    height = main_canvas.height();
    fitness_width = fitness_canvas.width();
    fitness_height = fitness_canvas.height();

    main_context.fillStyle = "rgb(100, 200, 250)";
    main_context.strokeStyle = "rgba(250, 50, 50, " + (1.0 / num_particles) + ")";
    main_context.lineWidth = 3;

    fitness_context.fillStyle = "rgb(100, 200, 250)";
    fitness_context.strokeStyle = "rgb(250, 50, 50)";

    initialize();

    window.setInterval(tick, 100);
    draw();
});