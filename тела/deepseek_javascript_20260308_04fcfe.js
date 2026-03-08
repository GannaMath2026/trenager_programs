import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

// Инициализация сцены
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x2d2d2d);

// Камера
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / 300, 0.1, 1000);
camera.position.set(5, 5, 5);
camera.lookAt(0, 0, 0);

// Рендерер WebGL
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('canvas'), antialias: true });
renderer.setSize(window.innerWidth - 300, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);

// Рендерер для текста
const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(window.innerWidth - 300, window.innerHeight);
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0px';
labelRenderer.domElement.style.left = '300px';
labelRenderer.domElement.style.pointerEvents = 'none';
document.body.appendChild(labelRenderer.domElement);

// Орбит контрол
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.autoRotate = true;
controls.autoRotateSpeed = 1.0;
controls.enableZoom = true;

// Освещение
const ambientLight = new THREE.AmbientLight(0x404060);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(1, 2, 1);
scene.add(directionalLight);

const backLight = new THREE.DirectionalLight(0xffffff, 0.5);
backLight.position.set(-1, -1, -1);
scene.add(backLight);

// Вспомогательные элементы
const gridHelper = new THREE.GridHelper(10, 20, 0x888888, 0x444444);
scene.add(gridHelper);

const axesHelper = new THREE.AxesHelper(5);
scene.add(axesHelper);

// Текущая модель
let currentModel = null;
let vertexLabels = [];
let edgeLines = [];

// Функция создания подписи вершины
function createVertexLabel(text, position, color = 'red') {
    const div = document.createElement('div');
    div.textContent = text;
    div.style.color = color;
    div.style.fontSize = '14px';
    div.style.fontWeight = 'bold';
    div.style.textShadow = '1px 1px 2px black';
    div.style.background = 'rgba(255,255,255,0.7)';
    div.style.padding = '2px 4px';
    div.style.borderRadius = '3px';
    div.style.border = '1px solid #333';
    
    const label = new CSS2DObject(div);
    label.position.copy(position);
    return label;
}

// Функция создания вершины (красная точка)
function createVertex(position) {
    const geometry = new THREE.SphereGeometry(0.1, 32, 16);
    const material = new THREE.MeshStandardMaterial({ color: 0xff3333, emissive: 0x330000 });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.copy(position);
    return sphere;
}

// Функция создания ребра (темно-синяя линия)
function createEdge(start, end) {
    const points = [start.clone(), end.clone()];
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({ color: 0x1a237e, linewidth: 2 });
    return new THREE.Line(geometry, material);
}

// Очистка предыдущей модели
function clearModel() {
    if (currentModel) {
        scene.remove(currentModel);
        currentModel = null;
    }
    
    vertexLabels.forEach(label => scene.remove(label));
    vertexLabels = [];
    
    edgeLines.forEach(line => scene.remove(line));
    edgeLines = [];
}

// Обновление списков вершин и рёбер
function updateInfo(vertices, edges) {
    const verticesList = document.getElementById('verticesList');
    const edgesList = document.getElementById('edgesList');
    
    verticesList.innerHTML = vertices.map((v, i) => 
        `<div>V${i}: (${v.x.toFixed(2)}, ${v.y.toFixed(2)}, ${v.z.toFixed(2)})</div>`
    ).join('');
    
    edgesList.innerHTML = edges.map((e, i) => 
        `<div>E${i}: V${e[0]} → V${e[1]}</div>`
    ).join('');
}

// Создание куба
function createCube() {
    const size = 2;
    const vertices = [
        new THREE.Vector3(-size/2, -size/2, -size/2),
        new THREE.Vector3( size/2, -size/2, -size/2),
        new THREE.Vector3( size/2,  size/2, -size/2),
        new THREE.Vector3(-size/2,  size/2, -size/2),
        new THREE.Vector3(-size/2, -size/2,  size/2),
        new THREE.Vector3( size/2, -size/2,  size/2),
        new THREE.Vector3( size/2,  size/2,  size/2),
        new THREE.Vector3(-size/2,  size/2,  size/2)
    ];
    
    const edges = [
        [0,1], [1,2], [2,3], [3,0],
        [4,5], [5,6], [6,7], [7,4],
        [0,4], [1,5], [2,6], [3,7]
    ];
    
    vertices.forEach((v, i) => {
        scene.add(createVertex(v));
        scene.add(createVertexLabel(`V${i}`, v));
        vertexLabels.push(...scene.children.slice(-2));
    });
    
    edges.forEach(edge => {
        const line = createEdge(vertices[edge[0]], vertices[edge[1]]);
        scene.add(line);
        edgeLines.push(line);
    });
    
    updateInfo(vertices, edges);
}

// Создание параллелепипеда
function createParallelepiped() {
    const vertices = [
        new THREE.Vector3(-1.5, -1, -1),
        new THREE.Vector3( 1.5, -1, -1),
        new THREE.Vector3( 1.5,  1, -1),
        new THREE.Vector3(-1.5,  1, -1),
        new THREE.Vector3(-1.5, -1,  1),
        new THREE.Vector3( 1.5, -1,  1),
        new THREE.Vector3( 1.5,  1,  1),
        new THREE.Vector3(-1.5,  1,  1)
    ];
    
    const edges = [
        [0,1], [1,2], [2,3], [3,0],
        [4,5], [5,6], [6,7], [7,4],
        [0,4], [1,5], [2,6], [3,7]
    ];
    
    vertices.forEach((v, i) => {
        scene.add(createVertex(v));
        scene.add(createVertexLabel(`V${i}`, v));
        vertexLabels.push(...scene.children.slice(-2));
    });
    
    edges.forEach(edge => {
        const line = createEdge(vertices[edge[0]], vertices[edge[1]]);
        scene.add(line);
        edgeLines.push(line);
    });
    
    updateInfo(vertices, edges);
}

// Создание треугольной призмы
function createTriangularPrism() {
    const height = 2;
    const radius = 1.5;
    
    const vertices = [
        new THREE.Vector3(radius, -height/2, 0),
        new THREE.Vector3(-radius/2, -height/2, radius*0.866),
        new THREE.Vector3(-radius/2, -height/2, -radius*0.866),
        new THREE.Vector3(radius,  height/2, 0),
        new THREE.Vector3(-radius/2,  height/2, radius*0.866),
        new THREE.Vector3(-radius/2,  height/2, -radius*0.866)
    ];
    
    const edges = [
        [0,1], [1,2], [2,0],
        [3,4], [4,5], [5,3],
        [0,3], [1,4], [2,5]
    ];
    
    vertices.forEach((v, i) => {
        scene.add(createVertex(v));
        scene.add(createVertexLabel(`V${i}`, v));
        vertexLabels.push(...scene.children.slice(-2));
    });
    
    edges.forEach(edge => {
        const line = createEdge(vertices[edge[0]], vertices[edge[1]]);
        scene.add(line);
        edgeLines.push(line);
    });
    
    updateInfo(vertices, edges);
}

// Создание четырёхугольной призмы
function createQuadrangularPrism() {
    const height = 2;
    const size = 1.5;
    
    const vertices = [
        new THREE.Vector3(-size, -height/2, -size),
        new THREE.Vector3( size, -height/2, -size),
        new THREE.Vector3( size, -height/2,  size),
        new THREE.Vector3(-size, -height/2,  size),
        new THREE.Vector3(-size,  height/2, -size),
        new THREE.Vector3( size,  height/2, -size),
        new THREE.Vector3( size,  height/2,  size),
        new THREE.Vector3(-size,  height/2,  size)
    ];
    
    const edges = [
        [0,1], [1,2], [2,3], [3,0],
        [4,5], [5,6], [6,7], [7,4],
        [0,4], [1,5], [2,6], [3,7]
    ];
    
    vertices.forEach((v, i) => {
        scene.add(createVertex(v));
        scene.add(createVertexLabel(`V${i}`, v));
        vertexLabels.push(...scene.children.slice(-2));
    });
    
    edges.forEach(edge => {
        const line = createEdge(vertices[edge[0]], vertices[edge[1]]);
        scene.add(line);
        edgeLines.push(line);
    });
    
    updateInfo(vertices, edges);
}

// Создание шестиугольной призмы
function createHexagonalPrism() {
    const height = 2;
    const radius = 1.5;
    const vertices = [];
    
    for (let i = 0; i < 6; i++) {
        const angle = (i * Math.PI / 3) - Math.PI / 6;
        vertices.push(new THREE.Vector3(
            radius * Math.cos(angle),
            -height/2,
            radius * Math.sin(angle)
        ));
    }
    
    for (let i = 0; i < 6; i++) {
        const angle = (i * Math.PI / 3) - Math.PI / 6;
        vertices.push(new THREE.Vector3(
            radius * Math.cos(angle),
            height/2,
            radius * Math.sin(angle)
        ));
    }
    
    const edges = [];
    // Нижнее основание
    for (let i = 0; i < 5; i++) edges.push([i, i+1]);
    edges.push([5, 0]);
    
    // Верхнее основание
    for (let i = 0; i < 5; i++) edges.push([i+6, i+7]);
    edges.push([11, 6]);
    
    // Боковые рёбра
    for (let i = 0; i < 6; i++) edges.push([i, i+6]);
    
    vertices.forEach((v, i) => {
        scene.add(createVertex(v));
        scene.add(createVertexLabel(`V${i}`, v));
        vertexLabels.push(...scene.children.slice(-2));
    });
    
    edges.forEach(edge => {
        const line = createEdge(vertices[edge[0]], vertices[edge[1]]);
        scene.add(line);
        edgeLines.push(line);
    });
    
    updateInfo(vertices, edges);
}

// Создание треугольной пирамиды
function createTriangularPyramid() {
    const height = 2;
    const radius = 1.5;
    
    const vertices = [
        new THREE.Vector3(radius, -height/2, 0),
        new THREE.Vector3(-radius/2, -height/2, radius*0.866),
        new THREE.Vector3(-radius/2, -height/2, -radius*0.866),
        new THREE.Vector3(0, height/2, 0)
    ];
    
    const edges = [
        [0,1], [1,2], [2,0],
        [0,3], [1,3], [2,3]
    ];
    
    vertices.forEach((v, i) => {
        scene.add(createVertex(v));
        scene.add(createVertexLabel(`V${i}`, v));
        vertexLabels.push(...scene.children.slice(-2));
    });
    
    edges.forEach(edge => {
        const line = createEdge(vertices[edge[0]], vertices[edge[1]]);
        scene.add(line);
        edgeLines.push(line);
    });
    
    updateInfo(vertices, edges);
}

// Создание четырёхугольной пирамиды
function createQuadrangularPyramid() {
    const height = 2;
    const size = 1.5;
    
    const vertices = [
        new THREE.Vector3(-size, -height/2, -size),
        new THREE.Vector3( size, -height/2, -size),
        new THREE.Vector3( size, -height/2,  size),
        new THREE.Vector3(-size, -height/2,  size),
        new THREE.Vector3(0, height/2, 0)
    ];
    
    const edges = [
        [0,1], [1,2], [2,3], [3,0],
        [0,4], [1,4], [2,4], [3,4]
    ];
    
    vertices.forEach((v, i) => {
        scene.add(createVertex(v));
        scene.add(createVertexLabel(`V${i}`, v));
        vertexLabels.push(...scene.children.slice(-2));
    });
    
    edges.forEach(edge => {
        const line = createEdge(vertices[edge[0]], vertices[edge[1]]);
        scene.add(line);
        edgeLines.push(line);
    });
    
    updateInfo(vertices, edges);
}

// Создание шестиугольной пирамиды
function createHexagonalPyramid() {
    const height = 2;
    const radius = 1.5;
    const vertices = [];
    
    for (let i = 0; i < 6; i++) {
        const angle = (i * Math.PI / 3) - Math.PI / 6;
        vertices.push(new THREE.Vector3(
            radius * Math.cos(angle),
            -height/2,
            radius * Math.sin(angle)
        ));
    }
    
    vertices.push(new THREE.Vector3(0, height/2, 0));
    
    const edges = [];
    // Основание
    for (let i = 0; i < 5; i++) edges.push([i, i+1]);
    edges.push([5, 0]);
    
    // Боковые рёбра к вершине
    for (let i = 0; i < 6; i++) edges.push([i, 6]);
    
    vertices.forEach((v, i) => {
        scene.add(createVertex(v));
        scene.add(createVertexLabel(`V${i}`, v));
        vertexLabels.push(...scene.children.slice(-2));
    });
    
    edges.forEach(edge => {
        const line = createEdge(vertices[edge[0]], vertices[edge[1]]);
        scene.add(line);
        edgeLines.push(line);
    });
    
    updateInfo(vertices, edges);
}

// Обработчик выбора фигуры
document.getElementById('shapeSelect').addEventListener('change', (e) => {
    const shape = e.target.value;
    clearModel();
    
    switch(shape) {
        case 'cube':
            createCube();
            break;
        case 'parallelepiped':
            createParallelepiped();
            break;
        case 'prism3':
            createTriangularPrism();
            break;
        case 'prism4':
            createQuadrangularPrism();
            break;
        case 'prism6':
            createHexagonalPrism();
            break;
        case 'pyramid3':
            createTriangularPyramid();
            break;
        case 'pyramid4':
            createQuadrangularPyramid();
            break;
        case 'pyramid6':
            createHexagonalPyramid();
            break;
    }
});

// Сброс вида
document.getElementById('resetView').addEventListener('click', () => {
    camera.position.set(5, 5, 5);
    camera.lookAt(0, 0, 0);
    controls.target.set(0, 0, 0);
    controls.autoRotate = true;
});

// Обработка изменения размера окна
window.addEventListener('resize', onWindowResize, false);
function onWindowResize() {
    camera.aspect = (window.innerWidth - 300) / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth - 300, window.innerHeight);
    labelRenderer.setSize(window.innerWidth - 300, window.innerHeight);
}

// Анимация
function animate() {
    requestAnimationFrame(animate);
    
    controls.update();
    
    renderer.render(scene, camera);
    labelRenderer.render(scene, camera);
}

animate();

// Показать куб по умолчанию
setTimeout(() => {
    createCube();
}, 100);