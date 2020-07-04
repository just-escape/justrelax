<template>
  <Window :title="'MENU'">
    <div class="d-flex flex-column justify-content-around align-items-center mx-4 h-100" style="font-size: 40px">
      TODO
      <span @click="cherche">cherche</span>
      <span @click="gratte">gratte</span>
      <!--<div class="d-flex flex-row justify-content-center">
        <ResearchComponent
          :shuffleSignal="components[0].shuffleSignal"
          :possibilities="components[0].possibilities"
          @stop="stop(0)"
        />
      </div>
      <div class="d-flex flex-row justify-content-around mb-5">
        <ResearchComponent
          :shuffleSignal="components[1].shuffleSignal"
          :possibilities="components[1].possibilities"
          @stop="stop(1)"
        />
        <ResearchComponent
          :shuffleSignal="components[2].shuffleSignal"
          :possibilities="components[2].possibilities"
          @stop="stop(2)"
        />
      </div>
      <div class="d-flex flex-row justify-content-center">
        <i class="fa fa-times"/>
      </div>-->
    </div>
  </Window>
</template>

<script>
import Window from '@/components/Window.vue'
// import ResearchComponent from '@/components/ResearchComponent.vue'
import businessStore from '@/store/businessStore.js'

export default {
  name: "ServicesWindow",
  components: {
    Window,
    // ResearchComponent,
  },
  data() {
    return {
      components: [
        {
          shuffleSignal: false,
          possibilities: [
            '<i class="fa fa-plus"/>',
            '<i class="fa fa-minus"/>',
            '<i class="fa fa-times"/>',
          ],
          shuffling: true,
        },
        {
          shuffleSignal: false,
          possibilities: [
            '<i class="fa fa-plus"/>',
            '<i class="fa fa-minus"/>',
            '<i class="fa fa-times"/>',
          ],
          shuffling: true,
        },
        {
          shuffleSignal: false,
          possibilities: [
            '<i class="fa fa-plus"/>',
            '<i class="fa fa-minus"/>',
            '<i class="fa fa-times"/>',
          ],
          shuffling: true,
        }
      ]
    }
  },
  methods: {
    shuffle() {
      for (var c of this.components) {
        c.shuffling = true
        c.shuffleSignal = !c.shuffleSignal
      }
    },
    stop(componentIndex) {
      this.components[componentIndex].shuffling = false
      if (
        this.components[0].shuffling === false &&
        this.components[1].shuffling === false &&
        this.components[2].shuffling === false
      ) {
        setTimeout(this.shuffle, 1000)
      }
    },
    click() {
      businessStore.commit('playMarmitronAnimation', 'reponse')
    },
    cherche() {
      businessStore.commit('playMarmitronAnimation', 'cherche')
    },
    gratte() {
      businessStore.commit('playMarmitronAnimation', 'gratte')
    },
  },
  mounted() {
    this.shuffle()
  },
}
</script>