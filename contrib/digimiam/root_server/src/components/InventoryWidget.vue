<template>
  <div>
    <div class="text-center" style="font-style: italic; font-size: 20px">Chambres des ingrédients</div>
    <div class="mt-4 position-relative">
      <HexagonChamber
        v-for="(chamber, chamberIndex) in chambers" :key="'chamber-' + chamberIndex"
        :top="chamber.top" :right="chamber.right" :width="70"
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
          },
          {
            top: 112,
            right: 60,
          },
          {
            top: 224,
            right: 60,
          },
          {
            top: 56,
            right: 157.5,
          },
          {
            top: 168,
            right: 157.5,
          },
          {
            top: 0,
            right: 255,
          },
          {
            top: 224,
            right: 255,
          },
          {
            top: 112,
            right: 255,
          },
        ]
      } else {
        return [
          {
            top: 0,
            right: 0,
          },
          {
            top: 100,
            right: 0,
          },
          {
            top: 200,
            right: 0,
          },
          {
            top: 50,
            right: 87,
          },
          {
            top: 250,
            right: 87,
          },
          {
            top: 0,
            right: 174,
          },
          {
            top: 200,
            right: 174,
          },
          {
            top: 200,
            right: 319,
          },
        ]
      }
    }
  }
}
</script>
