( function( api ) {

	// Extends our custom "better-health" section.
	api.sectionConstructor['better-health'] = api.Section.extend( {

		// No events for this type of section.
		attachEvents: function () {},

		// Always make the section active.
		isContextuallyActive: function () {
			return true;
		}
	} );

} )( wp.customize );
