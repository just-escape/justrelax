<template>
  <div :style="{filter: editable ? '' : 'grayscale(1)'}" class="transition-1s">
    <input :id="'checkbox-' + id" v-model="checked" type="checkbox" class="checkbox" />
    <label :for="editable ? 'checkbox-' + id : ''" class="switch" :style="{width: width + 'px', color: editable ? 'white' : 'gray'}" style="margin-bottom: 0">
        <span class="switch__circle">
          <span class="switch__circle-inner"></span>
        </span>
        <span class="switch__left">{{ offText }}</span>
        <span class="switch__right">{{ onText }}</span>
    </label>
  </div>
</template>

<script>
export default {
  name: "OnOffSwitch",
  data() {
    return {
      id: null,
      checked: true
    }
  },
  methods: {
    uuidv4() {
      return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
      )
    }
  },
  mounted() {
    this.id = this.uuidv4()
    this.checked = this.initiallyOn
  },
  props: {
    editable: {
      type: Boolean,
      default: true,
    },
    initiallyOn: {
      type: Boolean,
      default: true,
    },
    width: {
      type: Number,
      default: 70,
    },
    onText: {
      type: String,
      default: 'On',
    },
    offText: {
      type: String,
      default: 'Off',
    }
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.checkbox {
  display: none;
  position: relative;
}

.switch {
  align-items: center;
  border-radius: 500px;
  cursor: pointer;
  display: flex;
  height: 30px;
  justify-content: space-between;
  padding: 0 8px;
  position: relative;
  user-select: none;
  border: 2px solid rgb(0, 209, 182);
  box-shadow: 0px 0px 8px -3px rgba(0, 209, 182, 1);
}

.checkbox:checked ~ .switch {
  background-color: transparent;
}

.checkbox:not(:checked) ~ .switch {
  background-color: transparent;
}

.switch__left,
.switch__right {
  font-weight: bold;
  text-transform: uppercase;
}

.switch__right {
  position: absolute;
  right: 8px;
}

.checkbox:checked ~ .switch .switch__left {
  visibility: hidden;
}

.checkbox:not(:checked) ~ .switch .switch__right {
  visibility: hidden;
}

.switch__circle {
  height: 30px;
  padding: 5px;
  position: absolute;
  transition: all 0.5s ease-in-out;
  width: 30px;
}

.checkbox:checked ~ .switch .switch__circle {
  left: 0;
  right: calc(100% - 30px);
}

.checkbox:not(:checked) ~ .switch .switch__circle {
  left: calc(100% - 30px);
  right: 0;
}

.checkbox:checked ~ .switch .switch__circle .switch__circle-inner {
  box-shadow: 0px 0px 14px 2px rgb(0, 209, 182);
}

.checkbox:not(:checked) ~ .switch .switch__circle .switch__circle-inner {
  opacity: 0.7;
}

.switch__circle-inner {
  transition: all 0.5s ease-in-out;
  background-color: rgb(0, 209, 182);
  border-radius: 50%;
  display: block;
  height: 100%;
  width: 100%;
}
</style>