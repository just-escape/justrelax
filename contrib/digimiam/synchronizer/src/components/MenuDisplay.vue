<template>
  <div class="position-relative h-100">
    <div class="d-flex flex-column h-100">
      <div class="menu-container px-2 pb-1 position-relative h-100">
        <div class="menu-frame"></div>
        <div class="menu-background"></div>
        <div class="menu-title-ribbon mb-2 text-right p-2">
          <img src="@/assets/img/pyramid.svg" class="mb-1" height="18px"/> {{ $t('digimiam_menu') }}
        </div>
        <div class="date text-right mb-2 mt-2">
          {{ date }}
        </div>

        <div class="mb-5">
          <div class="d-flex flex-row justify-content-center mb-4" style="font-style: italic; font-size: 18px">
            <div>{{ $t('Plats du menu') }}</div>
          </div>
          <div class="position-relative d-flex flex-row justify-content-center mb-3">
            <div
              :key="item.id" v-for="item in menuItems"
              class="position-relative d-flex flex-row justify-content-center align-items-center transition-filter-2s"
              style="background: rgba(0, 209, 182, 0.6); width: 45px; height: 45px; margin: 0px 20px; font-size: 26px;"
              :style="{filter: filter(item)}"
            >
              <div class="position-absolute" style="top: 5px">
                {{ item.id }}
              </div>
              <div :style="{opacity: displayPrice ? 1 : 0}" class="position-absolute" style="bottom: -35px; font-size: 16px; transition: opacity 1s ease-in-out">
                {{ item.price }} nF
              </div>
            </div>
            <div
              class="position-absolute"
              style="border: 3px white solid; width: 61px; left: 39px; top: -16px; transition: left 1s ease-in-out, height 1s linear"
              :style="{left: cursorLeft + 'px', height: displayPrice ? '105px' : '80px'}"
            ></div>
          </div>
        </div>

        <div class="d-flex w-100 justify-content-center pt-2">
          <div
            class="text-center py-2 px-3"
            style="background: rgba(0, 209, 182, 0.6); transition: all 0.4s ease-in-out"
            :style="{opacity: displayHolographicUpdateOnChange ? holographicDisplayUpdatedOpacity : 0}"
          >
            <div>{{ $t('Affichage holographique modifié') }}</div>
          </div>
        </div>

        <div class="pt-3">
          <MenuLoadingWidget :startAnimationSignal="startAnimationSignal"/>
        </div>
        <div
          v-if="!menuSuccess && displayMenuExplicitInstruction"
          style="margin-top: 70px; background: rgba(255, 69, 0, 0.65); height: 104px"
          class="p-1 d-flex flex-row justify-content-center align-items-center pulse-opacity text-center"
        >
          <div v-if="priceMatters" v-html="$t('holographic_menu_dishes_price')"></div>
          <div v-else v-html="$t('holographic_menu_dishes')"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//import MenuItemCursor from '@/components/MenuItemCursor.vue'
import MenuLoadingWidget from '@/components/MenuLoadingWidget.vue'
//import MenuItem from '@/components/MenuItem.vue'
import menuStore from '@/store/menuStore.js'

export default {
  name: 'MenuDisplay',
  components: {
    // MenuItemCursor,
    MenuLoadingWidget,
    // MenuItem,
  },
  data() {
    return {
      date: undefined,
      startAnimationSignal: false,
      holographicDisplayUpdatedOpacity: 0,
      holographicDisplayUpdatedOpacityTask: null,
    }
  },
  computed: {
    displayHolographicUpdateOnChange() {
      return menuStore.state.displayHolographicUpdateOnChange
    },
    onMenuChangedSignal() {
      return menuStore.state.onMenuChangedSignal
    },
    displayMenuExplicitInstruction() {
      return menuStore.state.displayMenuExplicitInstruction
    },
    priceMatters() {
      return menuStore.state.priceMatters
    },
    validating() {
      return menuStore.state.validating
    },
    cursorLeft() {
      return menuStore.state.cursorPosition * 85 + 38
    },
    displayPrice() {
      return menuStore.state.displayPrice
    },
    dragging() {
      return menuStore.state.dragging
    },
    lang() {
      return this.$i18n.locale
    },
    menuItems() {
      return menuStore.state.menuItems
    },
    menuSuccess() {
      return menuStore.state.success
    },
    filter() {
      return (item) => {
        if (item.isDishValidated) {
          return 'hue-rotate(-40deg) brightness(0.65) contrast(0.95)'
        } else {
          return ''
        }
      }
    },
  },
  methods: {
    refreshDate() {
      var date = new Date()
      date.setFullYear(2080)
      this.$moment.locale(this.lang)
      this.date = this.$moment(date).format('LL')
    },
  },
  watch: {
    onMenuChangedSignal() {
      this.holographicDisplayUpdatedOpacity = 1
      clearTimeout(this.holographicDisplayUpdatedOpacityTask)
      this.holographicDisplayUpdatedOpacityTask = setTimeout((this_) => {this_.holographicDisplayUpdatedOpacity = 0}, 800, this)
    },
    validating(newValue) {
      if (newValue) {
        this.startAnimationSignal = !this.startAnimationSignal
      }
    },
    lang() {
      this.refreshDate()
    }
  },
  mounted() {
    this.refreshDate()
  }
}
</script>

<style scoped>
.menu-container {
  border: 1px solid transparent;
  border-top: 9px solid transparent;
  padding-top: 38px;
}

.menu-background {
  background-color: rgba(00, 45, 64, 0.5);
  position: absolute;
  top: -9px;
  left: -1px;
  right: -1px;
  bottom: -1px;
  clip-path: polygon(
    100% 0%,
    100% 100%,
    0% 100%,
    0px calc(43px - 6px),
    calc(43px + 6px) 0px
  );
  z-index: -1;
}

.menu-frame {
  position: absolute;
  left: -1px;
  top: -9px;
  right: -1px;
  bottom: -1px;
  filter: drop-shadow(1px 1px 4px rgba(0, 209, 182, 0.75));
  clip-path: polygon(
    calc(100% - 1px) -10px,
    calc(100% + 10px) -10px,
    calc(100% + 10px) calc(100% + 10px),
    -10px calc(100% + 6px),
    -10px calc(48px - 7px - 6px),
    calc(48px + 2px - 6px) -10px,
    calc(100% - 1px) -10px,
    calc(100% - 1px) 9px,
    calc(48px + 1px) 9px,
    1px 48px,
    1px calc(100% - 1px),
    calc(100% - 1px) calc(100% - 1px)
  );
  z-index: 1;
}

.menu-frame::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background-color: #00d1b6;
  clip-path: polygon(
    calc(100% - 1px) 0%,
    100% 0%,
    100% 100%,
    0% 100%,
    0% calc(48px - 7px),
    calc(48px + 2px) 0%,
    calc(100% - 1px) 0%,
    calc(100% - 1px) 9px,
    calc(48px + 1px) 9px,
    1px 48px,
    1px calc(100% - 1px),
    calc(100% - 1px) calc(100% - 1px)
  );
  z-index: 10;
}

.menu-title-ribbon {
  position: absolute;
  width: 100%;
  height: 40px;
  top: 0;
  right: 0;
  border-bottom: 1px solid #00d1b6;
  background-color: rgba(00, 45, 64, 0.6);
  font-size: 20px;
  clip-path: polygon(
    100% 0%,
    100% 100%,
    0% 100%,
    0px calc(43px - 9px),
    43px 0px
  );
}

.date {
  font-size: 14px;
  z-index: 11;
}

.transition-filter-2s {
  transition: filter 2s ease-in-out;
}
</style>
