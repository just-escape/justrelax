<template>
  <div class="position-absolute">
    <canvas id="container"></canvas>
  </div>
</template>

<script>
import * as THREE from 'three'

export default {
  name: 'PeriodicTable.vue',
  data: function() {
    return {
      camera: null,
      aspect: window.innerWidth / window.innerHeight,
      renderer: null,
      scene: null,
      controls: null,
    }
  },
  methods: {
    makeCube: function(x, y, z) {
      var geometry = new THREE.BoxBufferGeometry(50, 50, 50)
      var material = new THREE.MeshBasicMaterial({color: 0x00d1b6, opacity: 0.5, transparent: true})

      var mesh = new THREE.Mesh(geometry, material)
      mesh.position.set(x, y, z)

      this.scene.add(mesh)
    },
    init: function() {
      this.camera = new THREE.PerspectiveCamera(60, this.aspect, 1, 1000)
      this.camera.position.z = 500
      // world
      this.scene = new THREE.Scene()
      this.scene.background = new THREE.Color(0x03181f)
      this.scene.fog = new THREE.FogExp2(0x03181f, 0.002)
      var geometry = new THREE.BoxBufferGeometry(20, 20, 20)
      var material = new THREE.MeshPhysicalMaterial(
        {color: 0x00d1b6, flatShading: true, opacity: 0.5, transparent: true})
      for (var i = 0 ; i < 150 ; i ++) {
        var mesh = new THREE.Mesh(geometry, material)
        mesh.position.x = (Math.random() - 0.5) * 1000
        mesh.position.y = (Math.random() - 0.5) * 1000
        mesh.position.z = (Math.random() - 0.5) * 1000
        mesh.updateMatrix()
        mesh.matrixAutoUpdate = false
        this.scene.add(mesh)
      }
      // lights
      var light1 = new THREE.DirectionalLight(0xffffff)
      light1.position.set(1, 1, 1)
      this.scene.add(light1)
      var light2 = new THREE.DirectionalLight(0xffffff)
      light2.position.set(-1, -1, -1)
      this.scene.add(light2)
      var light3 = new THREE.AmbientLight(0xffffff)
      this.scene.add(light3)

      var canvas = document.getElementById('container')
      var context = canvas.getContext('webgl2')
      this.renderer = new THREE.WebGLRenderer({canvas: canvas, context: context})
      this.renderer.setPixelRatio(window.devicePixelRatio)
      this.renderer.setSize(window.innerWidth, window.innerHeight)

      window.addEventListener('resize', this.onWindowResize, false)
      this.render()

      var duration = 40000
      this.$anime.timeline({
        loop: true,
      })
      .add({
        targets: this.camera.position,
        x: -500,
        duration: duration,
        easing: 'easeOutSine',
      })
      .add({
        targets: this.camera.position,
        z: 0,
        duration: duration,
        update: this.render,
        easing: 'easeInSine',
      }, '-=' + duration)
      .add({
        targets: this.camera.position,
        x: 0,
        duration: duration,
        easing: 'easeInSine',
      })
      .add({
        targets: this.camera.position,
        z: -500,
        duration: duration,
        update: this.render,
        easing: 'easeOutSine',
      }, '-=' + duration)
      .add({
        targets: this.camera.position,
        x: 500,
        duration: duration,
        easing: 'easeOutSine',
      })
      .add({
        targets: this.camera.position,
        z: 0,
        duration: duration,
        update: this.render,
        easing: 'easeInSine',
      }, '-=' + duration)
      .add({
        targets: this.camera.position,
        x: 0,
        duration: duration,
        easing: 'easeInSine',
      })
      .add({
        targets: this.camera.position,
        z: 500,
        duration: duration,
        update: this.render,
        easing: 'easeOutSine',
      }, '-=' + duration)
    },
    onWindowResize: function() {
      this.camera.aspect = this.aspect
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(window.innerWidth, window.innerHeight)
      this.render()
    },
    render: function() {
      this.camera.lookAt(0, 0, 0)
			this.renderer.render(this.scene, this.camera)
    },
  },
  mounted() {
    this.init()
    this.render()
  }
}
</script>
