<template>
  <div>
    <div class="text-center" style="font-style: italic; font-size: 20px">Chambres des ingrédients</div>
    <div class="mt-4 position-relative">
      <HexagonChamber
        v-for="(chamber, chamberIndex) in chambers" :key="'chamber-' + chamberIndex"
        :top="chamber.top" :right="chamber.right" :width="70" :icon="chamber.icon"
      />
    </div>
  </div>
</template>

<script>
import HexagonChamber from "@/components/HexagonChamber.vue"

export default {
  name: "InventoryWidget",
  components: {
    HexagonChamber,
  },
  computed: {
    chambers() {
      let chambersVersion = this.$route.query.chambers_version

      if (chambersVersion && chambersVersion == 2) {
        return [
          {
            top: 0,
            right: 60,
            icon: require("@/assets/img/cinnamon.png"),
          },
          {
            top: 112,
            right: 60,
            icon: require("@/assets/img/insect.png"),
          },
          {
            top: 224,
            right: 60,
            icon: require("@/assets/img/beer.png"),
          },
          {
            top: 56,
            right: 157.5,
            icon: require("@/assets/img/lemon.png"),
          },
          {
            top: 168,
            right: 157.5,
            icon: require("@/assets/img/algua.png"),
          },
          {
            top: 0,
            right: 255,
            icon: require("@/assets/img/potatoe.png"),
          },
          {
            top: 224,
            right: 255,
            icon: require("@/assets/img/mint.png"),
          },
          {
            top: 112,
            right: 255,
            icon: require("@/assets/img/chocoffee.png"),
          },
        ]
      } else {
        return [
          {
            top: 0,
            right: 0,
            icon: require("@/assets/img/cinnamon.png"),
          },
          {
            top: 100,
            right: 0,
            icon: require("@/assets/img/mint.png"),
          },
          {
            top: 200,
            right: 0,
            icon: require("@/assets/img/chocoffee.png"),
          },
          {
            top: 50,
            right: 87,
            icon: require("@/assets/img/lemon.png"),
          },
          {
            top: 250,
            right: 87,
            icon: require("@/assets/img/beer.png"),
          },
          {
            top: 0,
            right: 174,
            icon: require("@/assets/img/potatoe.png"),
          },
          {
            top: 200,
            right: 174,
            icon: require("@/assets/img/algua.png"),
          },
          {
            top: 200,
            right: 319,
            icon: require("@/assets/img/insect.png"),
          },
        ]
      }
    }
  }
}
</script>
