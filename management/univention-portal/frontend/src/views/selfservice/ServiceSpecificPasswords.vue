<!--
  Copyright 2021-2022 Univention GmbH

  https://www.univention.de/

  All rights reserved.

  The source code of this program is made available
  under the terms of the GNU Affero General Public License version 3
  (GNU AGPL V3) as published by the Free Software Foundation.

  Binary versions of this program provided by Univention to you as
  well as other copyrighted, protected or trademarked materials like
  Logos, graphics, fonts, specific documentations and configurations,
  cryptographic keys etc. are subject to a license agreement between
  you and Univention and not subject to the GNU AGPL V3.

  In the case you use this program under the terms of the GNU AGPL V3,
  the program is provided in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU Affero General Public License for more details.

  You should have received a copy of the GNU Affero General Public
  License with the Debian GNU/Linux or Univention distribution in file
  /usr/share/common-licenses/AGPL-3; if not, see
  <https://www.gnu.org/licenses/>.
-->
<template>
  <guarded-site
    :title="TITLE"
    :subtitle="SUBTITLE"
    path="passwordreset/get_service_specific_passwords"
    :guarded-widgets="[]"
    :submit-label-after-loaded="SUBMIT_LABEL_AFTER_LOADED"
    @loaded="loaded"
    @save="setServiceSpecificPassword"
  >
    <div
      v-if="radiusPasswordSet"
      class="service-specific-passwords__hint"
    >
      {{ RADIUS_PASSWORD_SET }}
    </div>
    <div
      v-if="newRadiusPassword"
      class="service-specific-passwords__hint"
    >
      {{ NEW_RADIUS_PASSWORD_1 }}
      <pre>{{ newRadiusPassword }}</pre>
      {{ NEW_RADIUS_PASSWORD_2 }}
    </div>
  </guarded-site>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import { umcCommandWithStandby } from '@/jsHelper/umc';
import _ from '@/jsHelper/translate';
import GuardedSite from '@/views/selfservice/GuardedSite.vue';
import { WidgetDefinition } from '@/jsHelper/forms';

interface ServiceSpecificPasswordInfo {
  type: string,
  set: number,
}

interface Data {
  radiusPasswordSet: boolean,
  newRadiusPassword: '',
}

export default defineComponent({
  name: 'ProtectAccount',
  components: {
    GuardedSite,
  },
  data(): Data {
    return {
      radiusPasswordSet: false,
      newRadiusPassword: '',
    };
  },
  computed: {
    TITLE(): string {
      return _('Wireless LAN Password');
    },
    SUBTITLE(): string {
      return _('To login to the WLAN, you need a specific password. The password will be generated by the system and is valid until overwritten. You will be able to retrieve the password upon creation. A new password can be generated at any time, rendering the previous password invalid.');
    },
    SUBMIT_LABEL_AFTER_LOADED(): string {
      return _('Generate WLAN password');
    },
    RADIUS_PASSWORD_SET(): string {
      return _('You have already set a Wireless LAN password. You can overwrite it by clicking on the button below.');
    },
    NEW_RADIUS_PASSWORD_1(): string {
      return _('Your new password is:');
    },
    NEW_RADIUS_PASSWORD_2(): string {
      return _('Please add it to your device now. You will not be able to see it again.');
    },
  },
  methods: {
    loaded(result: ServiceSpecificPasswordInfo[]) {
      result.forEach((info) => {
        if (info.type === 'radius') {
          this.radiusPasswordSet = info.set > 0;
        }
      });
    },
    setServiceSpecificPassword(values) {
      umcCommandWithStandby(this.$store, 'passwordreset/set_service_specific_passwords', { ...values, password_type: 'radius' })
        .then((result) => {
          this.radiusPasswordSet = false;
          this.newRadiusPassword = result.password;
        })
        .catch((error) => {
          this.$store.dispatch('notifications/addErrorNotification', {
            title: _('Failed to set a password'),
            description: error.message,
          });
        });
    },
  },
});
</script>
<style lang="stylus">
.service-specific-passwords__hint
  margin: calc(2 * var(--layout-spacing-unit))
  pre
    overflow-x: auto
    padding: calc(2 * var(--layout-spacing-unit))
    background-color: var(--bgc-inputfield-on-container)
</style>
