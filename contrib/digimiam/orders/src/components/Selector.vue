<template>
  <div>
    <div id="container" class="w-100 h-100" style="background: black;">
      <!--<canvas id="canvas"></canvas>-->
      <!--<div id="canvas" style="background-color: black"></div>-->
      <!--<div class="col-6" style="background-color: blue">
      </div>
      <div class="col-3" style="background-color: green">
      </div>
      <div class="col-3" style="background-color: red">
      </div>-->
      <div v-for="(item, index) in items" :key="item.id" :id="'item-container-' + index" class="item-container media justify-content-end align-items-center">
        <div class="media-body d-flex flex-column text-right ">
          <div class="text text-right">
            {{ $t(item.id) }}
          </div>
          <div class="subtext">
            {{ $t(item.id + '_desc') }}
          </div>
        </div>
        <img src="@/assets/pizzage.png" width="160px" class="ml-4 img-fluid">
      </div>
    </div>
    <div id="menu">
      <button @click="transform(targets.table, 2000)" id="table">TABLE</button>
      <button @click="transform(targets.sphere, 2000)" id="sphere">SPHERE</button>
      <button @click="transform(targets.helix, 2000)" id="helix">HELIX</button>
      <button @click="transform(targets.grid, 2000)" id="grid">GRID</button>
    </div>
  </div>
</template>

<script>
import * as THREE from 'three'
import * as TWEEN from 'tween.js'
import { OrbitControls } from 'three-controls'
import { CSS3DRenderer, CSS3DObject } from 'three-css3drenderer'

export default {
  name: "Selector",
  data: function() {
    return {
      camera: null,
      renderer: null,
      scene: null,
      controls: null,
      objects: [],
      table: [
        "H", "Hydrogen", "1.00794", 1, 1,
        "He", "Helium", "4.002602", 18, 1,
        "Li", "Lithium", "6.941", 1, 2,
        "Be", "Beryllium", "9.012182", 2, 2,
        "B", "Boron", "10.811", 13, 2,
        "C", "Carbon", "12.0107", 14, 2,
        "N", "Nitrogen", "14.0067", 15, 2,
      ],
      items: [
        {
          id: "salade_flamande",
        },
        {
          id: "cambraisienne",
        },
        {
          id: "potjevleesch",
        },
        {
          id: "frites",
        },
        {
          id: "gaufresque",
        }
      ],
      targets: {
        table: [

        ],
        sphere: []
      },
    }
  },
  methods: {
    init: function() {
      let proportions = this.getContainerWidthAndHeight()
      this.camera = new THREE.PerspectiveCamera(40, proportions.width / proportions.height, 1, 10000)
      this.camera.position.z = 3000

      this.scene = new THREE.Scene()

      var container = document.getElementById('container')

      for (var i = 0 ; i < this.items.length ; i++) {
        /*var element = document.createElement( 'div' );
        element.className = 'element';
        element.style.backgroundColor = 'rgba(0,127,127,' + ( Math.random() * 0.5 + 0.25 ) + ')';

        var number = document.createElement( 'div' );
        number.className = 'number';
        number.textContent = ( i / 5 ) + 1;
        element.appendChild( number );

        var symbol = document.createElement( 'div' );
        symbol.className = 'symbol';
        symbol.textContent = this.table[ i ];
        element.appendChild( symbol );

        var details = document.createElement( 'div' );
        details.className = 'details';
        details.innerHTML = this.table[ i + 1 ] + '<br>' + this.table[ i + 2 ];
        element.appendChild( details );*/
        /*var itemContainer = document.createElement('div')
        element.className = 'item-container'
        
        var img = document.createElement('img')
        img.className = 'img-fluid'
        itemContainer.appendChild(img)*/
        var itemContainer = document.getElementById('item-container-' + i)

        var object = new CSS3DObject( itemContainer );
        object.position.x = Math.random() * 4000 - 2000;
        object.position.y = Math.random() * 4000 - 2000;
        object.position.z = Math.random() * 4000 - 2000;
        this.scene.add( object );

        this.objects.push( object );

        var object2 = new THREE.Object3D();
        object2.position.x = 0;
        object2.position.y = i * 200;
        this.targets.table.push( object2 );
      }

      var vector = new THREE.Vector3();
      for ( var i2 = 0, l = this.objects.length; i2 < l; i2 ++ ) {
        var phi = Math.acos( - 1 + ( 2 * i2 ) / l );
        var theta = Math.sqrt( l * Math.PI ) * phi;
        var object3 = new THREE.Object3D();
        object3.position.setFromSphericalCoords( 800, phi, theta );
        vector.copy( object3.position ).multiplyScalar( 2 );
        object3.lookAt( vector );
        this.targets.sphere.push( object3 );
      }

      // var context = canvas.getContext('webgl2')
      this.renderer = new CSS3DRenderer() // {canvas: canvas, context: context})
      this.renderer.setSize(proportions.width, proportions.height)
      container.appendChild(this.renderer.domElement)

      this.controls = new OrbitControls(this.camera, this.renderer.domElement)
      this.controls.enableZoom = false
      this.controls.enablePan = false
      this.controls.minAzimuthAngle = 0
      this.controls.maxAzimuthAngle = 0
      this.controls.enableDamping = true
      this.controls.dampingFactor = 0.05
      this.controls.rotateSpeed = 0.1
      // eslint-disable-next-line
      console.log(this.controls.dampingFactor)
      this.controls.addEventListener( 'change', this.render )

      this.transform( this.targets.table, 2000 )

      window.addEventListener('resize', this.onWindowResize, false)
    },
    transform: function(targets, duration) {
      TWEEN.removeAll()

      for ( var i = 0; i < this.objects.length; i ++ ) {
        var object = this.objects[ i ];
        var target = targets[ i ];
        new TWEEN.Tween( object.position )
          .to( { x: target.position.x, y: target.position.y, z: target.position.z }, Math.random() * duration + duration )
          .easing( TWEEN.Easing.Exponential.InOut )
          .start();
        new TWEEN.Tween( object.rotation )
          .to( { x: target.rotation.x, y: target.rotation.y, z: target.rotation.z }, Math.random() * duration + duration )
          .easing( TWEEN.Easing.Exponential.InOut )
          .start();
      }

      new TWEEN.Tween( this )
        .to( {}, duration * 2 )
        .onUpdate( this.render )
        .start();
    },
    getContainerWidthAndHeight: function() {
      let container = document.getElementById('container')
      return {width: container.offsetWidth, height: container.offsetHeight}
    },
    onWindowResize: function() {
      var proportions = this.getContainerWidthAndHeight()
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(proportions.width, proportions.height)
      this.render()
    },
    animate: function() {
      requestAnimationFrame(this.animate)
      TWEEN.update()
      this.controls.update()
    },
    render: function() {
      this.renderer.render(this.scene, this.camera)
    },
  },
  mounted() {
    this.init()
    this.animate()
  }
}
</script>

<style>
a {
  color: #8ff;
}

#menu {
  position: absolute;
  bottom: 20px;
  width: 100%;
  text-align: center;
}

.item-container {
  width: 700px;
  height: 160px;
  box-shadow: 0px 0px 12px rgba(0,255,255,0.5);
  border: 1px solid rgba(127,255,255,0.25);
  font-family: Helvetica, sans-serif;
  line-height: normal;
}

.item-container .text {
  font-size: 60px;
  font-weight: bold;
  color: rgba(255,255,255,0.75);
}

.item-container .subtext {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.75);
}

.element {
  width: 600px;
  height: 160px;
  box-shadow: 0px 0px 12px rgba(0,255,255,0.5);
  border: 1px solid rgba(127,255,255,0.25);
  font-family: Helvetica, sans-serif;
  text-align: center;
  line-height: normal;
  cursor: default;
}

.element:hover {
  box-shadow: 0px 0px 12px rgba(0,255,255,0.75);
  border: 1px solid rgba(127,255,255,0.75);
}

.element .number {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 12px;
  color: rgba(127,255,255,0.75);
}

.element .symbol {
  position: absolute;
  top: 40px;
  left: 0px;
  right: 0px;
  font-size: 60px;
  font-weight: bold;
  color: rgba(255,255,255,0.75);
  text-shadow: 0 0 10px rgba(0,255,255,0.95);
}

.element .details {
  position: absolute;
  bottom: 15px;
  left: 0px;
  right: 0px;
  font-size: 12px;
  color: rgba(127,255,255,0.75);
}

button {
  color: rgba(127,255,255,0.75);
  background: transparent;
  outline: 1px solid rgba(127,255,255,0.75);
  border: 0px;
  padding: 5px 10px;
  cursor: pointer;
}

button:hover {
  background-color: rgba(0,255,255,0.5);
}

button:active {
  color: #000000;
  background-color: rgba(0,255,255,0.75);
}
</style>
