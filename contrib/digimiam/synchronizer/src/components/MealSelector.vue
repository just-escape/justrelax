<template>
  <div class="d-flex h-100 d-flex flex-column mx-3">
    <div class="selector-frame glowing-container position-relative w-100 h-100 mb-3">
      <div class="synthetic">Synthetic</div>
      <div class="organic">Organic</div>
      <div class="yummy-yummy">Yummy yummy</div>
      <div class="yummy">Yummy</div>

      <MealToken
        v-for="(t, tokenIndex) in tokens"
        :key="t.id"
        :tokenIndex="tokenIndex"
      />

      <div v-for="row in selectableAreas" :key="row.id">
        <div v-for="col in row" :key="col.id" class="selectable-area" :style="{top: col.top, left: col.left}">
        </div>
      </div>
    </div>

    <div class="text-underline button-like-frame text-center generator-matrix-title">
      DISH GENERATOR MATRIX
    </div>
  </div>
</template>

<script>
import MealToken from '@/components/MealToken.vue'
import MenuStore from '@/store/MenuStore.js'

export default {
  name: 'MealSelectors2',
  components: {
    MealToken,
  },
  data: function() {
    return {
      selectableAreas: [
        [{top: "8%", left: "8%"}, {top: "8%", left: "31%"}, {top: "8%", left: "54%"}, {top: "8%", left: "77%"}],
        [{top: "31%", left: "8%"}, {top: "31%", left: "31%"}, {top: "31%", left: "54%"}, {top: "31%", left: "77%"}],
        [{top: "54%", left: "8%"}, {top: "54%", left: "31%"}, {top: "54%", left: "54%"}, {top: "54%", left: "77%"}],
        [{top: "77%", left: "8%"}, {top: "77%", left: "31%"}, {top: "77%", left: "54%"}, {top: "77%", left: "77%"}],
      ],
    }
  },
  computed: {
    tokens: function() {
      return MenuStore.state.tokens
    },
  },
}
</script>

<style scoped>

.synthetic {
  position: absolute;
  text-align: right;
  right: 0;
  bottom: calc(-14px - 5px);
  line-height: 1;
  font-size: 14px;
}

.organic {
  position: absolute;
  text-align: left;
  left: 0;
  bottom: calc(-14px - 5px);
  line-height: 1;
  font-size: 14px;
}

.yummy {
  position: absolute;
  bottom: 0;
  left: calc(-14px - 3px);
  writing-mode: tb-rl;
  transform: rotate(180deg);
  line-height: 1;
  font-size: 14px;
}

.yummy-yummy {
  position: absolute;
  top: 0;
  left: calc(-14px - 3px);
  writing-mode: tb-rl;
  transform: rotate(180deg);
  line-height: 1;
  font-size: 14px;
}

.selectable-area {
  position: absolute;
  border: 1px dotted rgba(255, 255, 255, 0.7);
  box-shadow: 0px 0px 14px -8px rgba(255, 255, 255, 1);
  height: 15%;
  width: 15%;
}

.selector-frame {
  height: 439px;
  width: 100%;
  background:
    linear-gradient(to right, transparent 15%, rgba(0, 150, 150, 0.09) 70%),
    linear-gradient(to top, transparent 15%, rgba(0, 150, 150, 0.09) 70%);
}

/* The same padding than on buttons */
.button-like-frame {
  padding: 0.375rem 0.75rem;
  height: 36px;
}

.generator-matrix-title {
  color: rgba(0, 209, 182, 0.7);
}
</style>